import pyodbc
from django.http import HttpResponse
from ..models import *
import environ
from random import randint, randrange
from datetime import timedelta, datetime

env = environ.Env()
environ.Env.read_env()
conn_string = 'DRIVER=' + env('PB_DRIVER') + \
              ';SERVER=tcp:' + env('PB_SERVER') + \
              ';PORT=80;DATABASE=' + env('PB_DATABASE') + \
              ';UID=' + env('PB_USERNAME') + \
              ';PWD=' + env('PB_PASSWORD')


def fetch_products(request):
    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT tw_Nazwa, tw_Symbol, "
                           "(SELECT SUM(st_Stan) from tw_stan WHERE st_TowId = tw_Id),"
                           "tw_Id,"
                           "tw_IdGrupa "
                           "FROM tw__Towar;")

            existing_ids = set(p.id for p in Product.objects.all())

            for row in cursor.fetchall():
                if existing_ids:
                    existing_ids.remove(int(row[3]))
                Product.objects.update_or_create(name=row[0], symbol=row[1], inventory=int(row[2]), id=int(row[3]),
                                                 group=Group.objects.get(id=int(row[4])), is_archived=False)

            for removed_id in existing_ids:
                Product.objects.get(id=removed_id).is_archived = True

    return HttpResponse("Products fetched!")


def fetch_groups(request):
    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("select grt_Id, grt_Nazwa from sl_GrupaTw;")
            for row in cursor.fetchall():
                Group.objects.update_or_create(id=int(row[0]), name=row[1])

    return HttpResponse("Groups fetched!")


def fetch_features_dict(request):
    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ctw_Id, ctw_Nazwa FROM sl_CechaTw;")
            for row in cursor.fetchall():
                Feature.objects.update_or_create(id=int(row[0]), name=row[1])

    return HttpResponse("Features dict fetched!")


def fetch_product_features_dependencies(request):
    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT cht_Id, cht_IdTowar, cht_IdCecha FROM tw_CechaTw;")
            for row in cursor.fetchall():
                product = Product.objects.get(id=int(row[1]))
                feature = Feature.objects.get(id=int(row[2]))
                ProductFeature.objects.update_or_create(id=int(row[0]), product=product, feature=feature)

    return HttpResponse("Product-features dependencies fetched!")


def fetch_documents(request):
    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT dok_Id, dok_Typ, dok_MagId, dok_DataWyst  FROM dok__Dokument;")
            for row in cursor.fetchall():
                warehouse = Warehouse.objects.get(id=int(row[2]))
                Document.objects.update_or_create(id=int(row[0]), type=int(row[1]), warehouse=warehouse,
                                                  datetime=row[3])

    return HttpResponse("Documents fetched!")


def fetch_documents_items(request):
    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ob_Id, ob_TowId, ob_Ilosc, ob_Znak, ob_DokHanId, ob_DokMagId FROM dok_Pozycja;")
            for row in cursor.fetchall():
                product = Product.objects.get(id=int(row[1]))
                Item.objects.update_or_create(id=int(row[0]), product=product, amount=int(row[2]), sign=int(row[3]))

                for i in [4, 5]:  # "ob_DokHanId, ob_DokMagId"
                    if row[i]:
                        doc_items = Document.objects.get(id=int(row[i])).items
                        if not doc_items.filter(id=int(row[i])).exists():
                            doc_items.add(int(row[0]))

    return HttpResponse("Documents items fetched!")


def random_date():
    return datetime.strptime('1/1/2020', '%m/%d/%Y') + timedelta(seconds=randrange(10 ** 5, 10 ** 6))


# invoked while fetching all data or manually ("stock_management/populate/predictions/"), just for development purposes
def populate_predictions(request):
    for pr in Product.objects.all():
        for wh in Warehouse.objects.all():
            Prediction.objects.create(product=pr, value=randint(1, 100), warehouse=wh, date=random_date())

    return HttpResponse("Predictions table populated!")


def fetch_warehouses(request):
    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT mag_Id, mag_Symbol, mag_Nazwa FROM sl_Magazyn;")
            for row in cursor.fetchall():
                Warehouse.objects.update_or_create(id=int(row[0]), symbol=row[1], name=row[2])

    return HttpResponse("Warehouses fetched!")


def fetch_all_data(request):
    fetch_groups(request)
    fetch_features_dict(request)
    fetch_products(request)
    fetch_product_features_dependencies(request)
    fetch_warehouses(request)
    fetch_documents(request)
    fetch_documents_items(request)
    populate_predictions(request)

    return HttpResponse("All data fetched! Predictions were also made.")