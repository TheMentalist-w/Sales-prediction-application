import pyodbc
from django.http import HttpResponse
from ..models import Product, Group, Feature, ProductFeature, Document, Place
import environ

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
                if existing_ids :
                    existing_ids.remove(int(row[3]))
                Product.objects.update_or_create(name=row[0], symbol=row[1], inventory=int(row[2]), id=int(row[3]), group=Group.objects.get(id=int(row[4])),is_archived=False)

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

    return HttpResponse(f"Features dict fetched!")


def fetch_product_features_dependencies(request):
    with pyodbc.connect(conn_string) as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT cht_Id, cht_IdTowar, cht_IdCecha FROM tw_CechaTw;")
            for row in cursor.fetchall():
                product = Product.objects.get(id=int(row[1]))
                feature = Feature.objects.get(id=int(row[2]))
                ProductFeature.objects.update_or_create(id=int(row[0]), product=product, feature=feature)

    return HttpResponse(f"Product-features dependencies fetched!")


def fetch_documents(request):
    with pyodbc.connect(conn_string) as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT dok_Id, dok_Typ, dok_MscWyst, dok_DataWyst  FROM dok__Dokument;")
            for row in cursor.fetchall():

                if not Place.objects.filter(name=row[2]).exists():
                    place = Place.objects.update_or_create(name=row[2])
                else:
                    place = Place.objects.get(name=row[2])

                Document.objects.update_or_create(id=int(row[0]), type=int(row[1]), place=place, datetime=row[3])

    return HttpResponse(f"Documents fetched!")


def fetch_all_data(request):
    fetch_groups(request)
    fetch_features_dict(request)
    fetch_products(request)
    fetch_product_features_dependencies(request)
    return HttpResponse("All data fetched!")