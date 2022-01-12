import random
from datetime import datetime, timezone, timedelta
from random import sample

import numpy as np
from django.http import HttpResponse
from django.db.models import Max
import joblib
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras import Sequential
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

from ..models import *

def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true)))


MAX_SEARCH_DAYS = 180  # for optimization purposes


def get_historical_sales(prod_id, warehouse_id, target_date):
    res = {'last_week': 0, 'last_two_weeks': 0, 'last_month': 0, 'last_three_months': 0, 'last_six_months': 0}

    for doc in Document.objects.filter(type__in=[11, 13, 35]).filter(warehouse=warehouse_id,
                                        datetime__gte=target_date-timedelta(days=MAX_SEARCH_DAYS),
                                        datetime__lt=target_date).order_by('datetime'):  # doc types: 36+, 14+, 10+, 12+, 11-, 13-, 35-, 9
        days_passed = (target_date - doc.datetime).days
        for item in doc.items.all():
            if item.product.id == prod_id:
                if days_passed <= 7:
                    res['last_week'] += item.amount
                if days_passed <= 14:
                    res['last_two_weeks'] += item.amount
                if days_passed <= 30:
                    res['last_month'] += item.amount
                if days_passed <= 90:
                    res['last_three_months'] += item.amount
                if days_passed <= MAX_SEARCH_DAYS:
                    res['last_six_months'] += item.amount

    return res


def get_sales_days(prod_id, warehouse_id, start_amount, start_date):

    for doc in Document.objects.filter(type__in=[11, 13, 35, 9], datetime__gt=start_date, warehouse=warehouse_id).order_by('datetime'):  # doc types: 36+, 14+, 10+, 12+, 11-, 13-, 35-
        for item in doc.items.all():
            if item.product.id == prod_id:

                if doc.type == 9:       # stock transfer between warehouses
                    if doc.warehouse.id == warehouse_id:    # outgoing transfer
                        start_amount += item.amount
                    if doc.receiver == warehouse_id:   # incoming transfer
                        start_amount -= item.amount

                else:                   # 'ordinary' sales
                    start_amount -= item.amount

                if start_amount <= 0:
                    return float((doc.datetime - start_date).days)
    return None

def append_to_ai_array(append_x, append_y):

    arr = NeuralNetworkInputArray.objects.filter(id=1)

    if arr.exists():
        arr = arr.first()
        arr.x.append(append_x)
        arr.y.append(append_y)
        arr.save()
    else:
        NeuralNetworkInputArray.objects.create(id=1, x=[append_x], y=[append_y])


def reset_ai_array():
    NeuralNetworkInputArray.objects.filter(id=1).delete()


# mode = 0 deletes existing NN input array and create new based on ALL documents
# mode = 1 updates existing NN input array, creating entries based on docs from last 24h
def prepare_prediction_data(mode):

    # HEADERS:
    # x = [['delivery_amount', 'last_week_sales', 'last_two_weeks_sales', 'last_month_sales', 'last_three_months_sales','last_six_months_sales', 'month', 'mag_id'] + \
    #     [feature.id for feature in Feature.objects.order_by('id')]]
    # y = [['expected_output']]

    if mode not in [0, 1]:
        raise ValueError(f"Please enter valid NN array preparing mode (0 for INIT/ 1 for UPDATE) [mode given={mode}]")

    if mode == 0:
        reset_ai_array()

    docs_to_process = Document.objects.filter(type__in=[36, 14, 10, 12])    # doc types: 36+, 14+, 10+, 12+, 11-, 13-, 35-

    if mode == 1:
        docs_to_process = docs_to_process.filter(datetime__gt=datetime.now(timezone.utc)-timedelta(hours=24))  # if in 1 (UPDATE) mode,
                                                                                                               # process only docs from last 24h

    num_of_docs = docs_to_process.count()
    print(f"Num of docs to process: {num_of_docs}")

    i = 0
    for doc in docs_to_process.order_by('?')[:500]:   # use .order_by('?')[:num_of samples] if in 0 (INIT) mode and execution time is too long

        print(f"Processing doc {i} out of {num_of_docs}")

        for item in doc.items.all():
            sales_days = get_sales_days(prod_id=item.product.id, warehouse_id=doc.warehouse,    # expected output (y1, y2, y3...)
                                        start_amount=item.amount, start_date=doc.datetime)

            if sales_days is not None:  # skip items that have not been given out yet

                neural_variables = [item.amount] + \
                list(get_historical_sales(prod_id=item.product.id,
                                          warehouse_id=doc.warehouse,
                                          target_date=doc.datetime).values()) + \
                [int(doc.datetime.strftime('%m')), doc.warehouse.id] + \
                [1 if fea in item.product.features.all() else 0 for fea in Feature.objects.all()] # variables of neural network (x1, x2, x3...)

                append_to_ai_array(append_x=neural_variables, append_y=sales_days)      # save partial result to DB
                print(neural_variables, sales_days)                                     # and print it

        i += 1

    return HttpResponse("Input prediction array updated!")


def train_model(request):
    # load input data

    arr = NeuralNetworkInputArray.objects.filter(id=1)

    if not arr.exists():
        return HttpResponse("Can't train model, because AI input array does not exist!", 404)
    else:
        arr = arr.first()

    x, y = arr.x, arr.y

    x_train, y_train, x_val, y_val = [], [], [], []

    # create training and validation sets
    chosen_ids = sample(range(len(x)), int(0.1 * len(x)))   # generate (30% * num_of_input_rows) indexes
                                                            # to add them to validation set

    for i in range(len(x)):
        if i in chosen_ids:
            x_val.append(x[i])
            y_val.append(y[i])
        else:
            x_train.append(x[i])
            y_train.append(y[i])

    x_train, y_train, x_val, y_val = np.asarray(x_train), np.asarray(y_train), \
                                     np.asarray(x_val), np.asarray(y_val)

    print(f"Size of training set:{len(x_train)}, of validation set:{len(x_val)}")


    """
    # print input data
    print("Training set:")
    for i, j in zip(x_train, y_train):
        print(i, j)

    print("Validation set:")
    for i, j in zip(x_val, y_val):
        print(i, j)
    """

    print(x_train[0],y_train[0])

    scaler = MinMaxScaler()
    scaler.fit(x_train)

    #save scaler to file
    joblib.dump(scaler, "scaler.save")

    x_train = scaler.transform(x_train)
    x_val = scaler.transform(x_val)

    """
    # print normalized data
    print("Normalized training set:")
    for i, j in zip(x_train, y_train):
        print(i, j)

    print("Normalized validation set:")
    for i, j in zip(x_val, y_val):
        print(i, j)
    """

    print(x_train[0], y_train[0])

    # create model
    model = Sequential()

    model.add(Dense(256, input_dim=(len(x_train[0])), activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(1, activation='relu'))

    # compile model
    model.compile(
        loss=rmse,
        optimizer=Adam(),
        metrics=[rmse]
    )

    # train model
    model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=10**3) # ,verbose=0

    # validate model

    predictions = np.ravel(model.predict(x_val))
    err = rmse(y_val, predictions).numpy()

    print(predictions, err)

    # print summary and save model to file
    model.summary()
    model.save('pitbull_ai_model.h5')

    return HttpResponse("Done!")


def make_predictions(request):
    # load model
    model = load_model('pitbull_ai_model.h5', compile=False)
    scaler = joblib.load("scaler.save")

    # calculate 'inventory' normalization rate
    inventory_norm_rate = max([el[0] for el in NeuralNetworkInputArray.objects.filter(id=1).first().x]) \
                / Product.objects.aggregate(Max('inventory'))['inventory__max']

    for p in Product.objects.all():
        for w in Warehouse.objects.all():

            arr = [
                [p.inventory*inventory_norm_rate] + \
                list(get_historical_sales(prod_id=p.id,
                                          warehouse_id=w.id,
                                          target_date=datetime.now(timezone.utc)).values()) + \
                  [int(datetime.now().strftime('%m')), w.id] + \
                  [1 if f in p.features.all() else 0 for f in Feature.objects.all()]
                ]

            # normalize input data
            scaled_arr = scaler.transform(arr)

            # make prediction, print and save it
            prediction = int(np.ravel(model.predict(scaled_arr))[0])
            print(f"{p.name}, warehouse {w.name}, neural network result: {prediction} days")

            if not 0 < prediction < 1200:
                print("Unexpected output, changing prediction's value to None!")
                prediction = None

            Prediction.objects.create(product=p, value=prediction, warehouse=w, date=datetime.now(timezone.utc))

    return HttpResponse("Done!")


def update_nn_array(request):
    prepare_prediction_data(mode=1)
    return HttpResponse("Done!")


# mode = 0 deletes existing NN input array and create new based on ALL documents
# mode = 1 updates existing NN input array, creating entries based on docs from last 24h

def update_train_predict(request):

    # prepare_prediction_data(mode=1)
    # train_model(request)
    make_predictions(request)

    return HttpResponse("Done!")


def init_train_predict(request):

    prepare_prediction_data(mode=0)
    train_model(request)
    make_predictions(request)

    return HttpResponse("Done!")
