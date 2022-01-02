from django.http import HttpResponse
from statsmodels.tools.eval_measures import rmse
import numpy as np


from ..models import *
from datetime import datetime

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend as K


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
    x = [['curr_inventory', 'last_week_sales', 'last_two_weeks_sales', 'last_month_sales', 'month', 'mag_id'] + \
         [feature.name for feature in Feature.objects.order_by('id')]]
    y = [['expected_output']]

    for doc in Document.objects.filter(type__in=[36, 14, 10]):  # doc types: 36+, 14+, 10+, 12+, 11-, 13-, 35-
        print(f"Processing doc id={doc.id}")
        for item in doc.items.all():

            sales_days = get_sales_days(prod_id=item.product.id, start_amount=item.amount, start_date=doc.datetime)

            if sales_days is not None:  # skip items that have not given out yet

                y.append(sales_days)

                x.append(
                    [item.product.inventory] +
                    list(get_historical_sales(prod_id=item.product.id,
                                              target_date=datetime.fromisoformat('2021-09-11T04:16:13-04:00')).values()) +
                    [int(doc.datetime.strftime('%m')), doc.warehouse.id] +
                    get_boolean_item_features(item)
                )

    arr = NeuralNetworkInputArray.objects.filter(id=1)
    if arr.exists():
        arr.update(x=x, y=y)
    else:
        NeuralNetworkInputArray.objects.create(id=1, x=x, y=y)

    return HttpResponse("Input prediction array updated!")


def train_model(request):

    # load input data

    arr= NeuralNetworkInputArray.objects.filter(id=1)

    if not arr.exists():
        return HttpResponse("Can't train model, because AI input array does not exist!", 404)
    else:
        arr = arr.first()

    x_train, y_train = arr.x, arr.y

    for i, j in zip(x_train, y_train):
        print(i, j)

    # skip headers
    x_train, y_train = x_train[1:], y_train[1:]

    # build model
    model = Sequential()

    model.add(Dense((len(x_train[0])), activation='relu'))       # input layer
    model.add(Dense(32, activation='relu'))  # hidden layer
    model.add(Dense(1, activation='relu'))  # output layer

    # compile model
    model.compile(
        loss=rmse,
        optimizer=Adam(),
        metrics=[rmse]
    )

    # train model
    model.fit(x_train, y_train, epochs=250)

    model.summary()
    model.save('pitbull-AI')

    # TODO validate model

    # x_validate = [[508, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 0, 0],
    #               [510, 0, 0, 50, 2, 1, 1, 1, 1, 1, 0, 1, 0]]
    #
    # y_validate = [7.0, 7.0]

    # make predictions and calculate error

    x_test = [[510, 0, 0, 50, 2, 1, 1, 1, 1, 1, 0, 1, 0]]
    y_test = [7.0]

    predictions = np.ravel(model.predict(x_test))

    err = rmse(y_test, predictions).numpy()

    print(predictions, err)

    return HttpResponse("Done!")