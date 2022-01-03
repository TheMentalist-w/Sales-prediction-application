from datetime import datetime
from random import sample

import matplotlib.pyplot as plt
import numpy as np
from django.http import HttpResponse
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tools.eval_measures import rmse
from tensorflow.keras import Sequential
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

from ..models import *


# from stackoverflow
def plot_preds(traindata,
               trainlabels,
               testdata,
               testlabels,
               predictions):
    plt.figure(figsize=(12, 6))
    plt.scatter(traindata, trainlabels, c="b", label="Training data")
    plt.scatter(testdata, testlabels, c="g", label="Testing data")
    plt.scatter(testdata, predictions, c="r", label="Predictions")
    plt.legend()


def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true)))


def get_historical_sales(prod_id, target_date):
    res = {'last_week': 0, 'last_two_weeks': 0, 'last_month': 0}

    for doc in Document.objects.filter(type__in=[11, 13, 35]):  # doc types: 36+, 14+, 10+, 12+, 11-, 13-, 35-, 9
        for item in doc.items.all():
            if item.product.id == prod_id:
                days_passed = (target_date - doc.datetime).days
                if days_passed <= 7:
                    res['last_week'] += item.amount
                if days_passed <= 14:
                    res['last_two_weeks'] += item.amount
                if days_passed <= 30:
                    res['last_month'] += item.amount

                # if 360 <= days_passed <= 360:
                #    res['last_month'] += item.amount

    return res


def get_sales_days(prod_id, start_amount, start_date):
    for doc in Document.objects.filter(type__in=[11, 13, 35], datetime__gt=start_date).order_by(
            'datetime'):  # doc types: 36+, 14+, 10+, 12+, 11-, 13-, 35-
        for item in doc.items.all():
            if item.product.id == prod_id:
                start_amount -= item.amount
                if start_amount <= 0:
                    return float((doc.datetime - start_date).days)
    return None


def get_boolean_item_features(item):
    features_boolean = []

    for feature in Feature.objects.order_by('id'):
        if feature in item.product.features.all():
            features_boolean.append(0)
        else:
            features_boolean.append(1)

    return features_boolean


def update_prediction_data(request):
    # HEADERS:
    # x = [['curr_inventory', 'last_week_sales', 'last_two_weeks_sales', 'last_month_sales', 'month', 'mag_id'] + \
    #     [feature.name for feature in Feature.objects.order_by('id')]]
    # y = [['expected_output']]

    x, y = [], []

    for doc in Document.objects.filter(type__in=[36, 14, 10]):  # doc types: 36+, 14+, 10+, 12+, 11-, 13-, 35-
        print(f"Processing doc id={doc.id}")
        for item in doc.items.all():

            sales_days = get_sales_days(prod_id=item.product.id, start_amount=item.amount, start_date=doc.datetime)

            if sales_days is not None:  # skip items that have not given out yet

                y.append(sales_days)

                x.append(
                    [item.product.inventory] +
                    list(get_historical_sales(prod_id=item.product.id,
                                              target_date=datetime.fromisoformat(
                                                  '2021-09-11T04:16:13-04:00')).values()) +
                    [int(doc.datetime.strftime('%m')), doc.warehouse.id] +
                    get_boolean_item_features(item)
                )

    x_train, y_train, x_val, y_val = [], [], [], []

    # create training and validation sets
    chosen_ids = sample(range(len(x)), int(0.3 * len(x)))  # generate (30% * num_of_input_rows) indexes
                                                            # to add them to validation set

    for i in range(len(x)):
        if i in chosen_ids:
            x_val.append(x[i])
            y_val.append(y[i])
        else:
            x_train.append(x[i])
            y_train.append(y[i])

    arr = NeuralNetworkInputArray.objects.filter(id=1)
    if arr.exists():
        arr.update(x_train=x_train, y_train=y_train, x_val=x_val, y_val=y_val)
    else:
        NeuralNetworkInputArray.objects.create(id=1, x_train=x_train, y_train=y_train, x_val=x_val, y_val=y_val)

    return HttpResponse("Input prediction array updated!")


def train_model(request):
    # load input data

    arr = NeuralNetworkInputArray.objects.filter(id=1)

    if not arr.exists():
        return HttpResponse("Can't train model, because AI input array does not exist!", 404)
    else:
        arr = arr.first()

    x_train, y_train, x_val, y_val = np.asarray(arr.x_train), np.asarray(arr.y_train), \
                                     np.asarray(arr.x_val), np.asarray(arr.y_val)

    print(f"Size of training set:{len(x_train)}, of validation set:{len(x_val)}")


    
    # print input data
    print("Training set:")
    for i, j in zip(x_train, y_train):
        print(i, j)

    print("Validation set:")
    for i, j in zip(x_val, y_val):
        print(i, j)
        


    # normalize data and convert to numpy array
    # x_train, y_train, x_val, y_val = normalize(x_train, axis=0, norm='max'), np.asarray(y_train), \
    #                                  normalize(x_val, axis=0, norm='max'), np.asarray(y_val)

    scaler = MinMaxScaler()
    scaler.fit(x_train)

    #save scaler to file
    joblib.dump(scaler, "scaler.save")


    x_train = scaler.transform(x_train)
    x_val = scaler.transform(x_val)


    
    # print normalized data
    print("Normalized training set:")
    for i, j in zip(x_train, y_train):
        print(i, j)

    print("Normalized validation set:")
    for i, j in zip(x_val, y_val):
        print(i, j)



    # create model
    model = Sequential()

    model.add(Dense(20, input_dim=(len(x_train[0])), activation='relu'))  # input layer
    model.add(Dense(64, activation='relu'))  # hidden layer
    model.add(Dense(1, activation='linear'))  # output layer

    # compile model
    model.compile(
        loss=rmse,
        optimizer=Adam(),
        metrics=[rmse]
    )

    # train model
    model.fit(x_train, y_train, epochs=10**4) # ,verbose=0

    # validate model

    x_validate = [[508, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 0, 0],
                  [510, 0, 0, 50, 2, 1, 1, 1, 1, 1, 0, 1, 0]]

    y_validate = [7.0, 7.0]

    x_validate, y_validate = scaler.transform(x_validate), np.asarray(y_validate)

    predictions = np.ravel(model.predict(x_validate))

    err = rmse(y_validate, predictions).numpy()

    print(predictions, err)

    # print summary and save model to file
    model.summary()
    model.save('pitbull_ai_model.h5')

    return HttpResponse("Done!")


def make_predictions(request):
    # load model
    model = load_model('pitbull_ai_model.h5', compile=False)

    # make predictions and calculate error

    x_test = np.array([[510, 0, 0, 50, 2, 1, 1, 1, 1, 1, 0, 1, 0]])
    y_test = [7.0]

    # normalize input data
    scaler = joblib.load("scaler.save")
    x_test = scaler.transform(x_test)

    predictions = np.ravel(model.predict(x_test))

    err = rmse(y_test, predictions).numpy()

    print(predictions, err)

    return HttpResponse("Done!")
