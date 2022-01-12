import environ
import pyodbc
from django.http import HttpResponse
from django.utils.timezone import make_aware

from ..models import *

env = environ.Env()
environ.Env.read_env()
conn_string = 'DRIVER=' + env('PB_DRIVER') + \
              ';SERVER=tcp:' + env('PB_SERVER') + \
              ';PORT=80;DATABASE=' + env('PB_DATABASE') + \
              ';UID=' + env('PB_USERNAME') + \
              ';PWD=' + env('PB_PASSWORD')


def fetch_products():
    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT tw_Nazwa, tw_Symbol, "
                           "(SELECT SUM(st_Stan) from t_stan WHERE st_TowId = tw_Id),"
                           "tw_Id,"
                           "tw_IdGrupa "
                           "FROM t_Towar;")

            existing_ids = set(p.id for p in Product.objects.all())

            for row in cursor.fetchall():
                if existing_ids :
                    existing_ids.remove(int(row[3]))
                Product.objects.update_or_create(id=int(row[3]), defaults={'name': row[0], 'symbol': row[1], 'inventory': 0 if row[2] is None else int(row[2]), 'id': int(row[3]), 'group': Group.objects.get(id=int(row[4])),'is_archived': False})

            for removed_id in existing_ids:
                Product.objects.get(id=removed_id).is_archived = True

    return HttpResponse("Products fetched!")


def fetch_groups():
    with pyodbc.connect(conn_string) as conn:

        with conn.cursor() as cursor:
            cursor.execute("select grt_Id, grt_Nazwa from s_GrupaTw;")
            for row in cursor.fetchall():
                Group.objects.update_or_create(id=int(row[0]), defaults={'id': int(row[0]), 'name': row[1]})

    return HttpResponse("Groups fetched!")


def fetch_features_dict():
    with pyodbc.connect(conn_string) as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT ctw_Id, ctw_Nazwa FROM s_CechaTw;")
            for row in cursor.fetchall():
                Feature.objects.update_or_create(id=int(row[0]), defaults={'id': int(row[0]), 'name': row[1]})

    return HttpResponse("Features dict fetched!")


def fetch_product_features_dependencies():
    with pyodbc.connect(conn_string) as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT cht_Id, cht_IdTowar, cht_IdCecha FROM t_CechaTw;")
            for row in cursor.fetchall():
                product = Product.objects.get(id=int(row[1]))
                feature = Feature.objects.get(id=int(row[2]))
                ProductFeature.objects.update_or_create(id=int(row[0]), defaults={'id':int(row[0]), 'product': product, 'feature': feature})

    return HttpResponse("Product-features dependencies fetched!")


def fetch_documents():
    with pyodbc.connect(conn_string) as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT dok_Id, dok_Typ, dok_MagId, dok_DataWyst, dok_OdbiorcaId  FROM d_Dokument;")
            for row in cursor.fetchall():
                print(f"Fetching docs, id={int(row[0])}")
                warehouse = Warehouse.objects.get(id=int(row[2]))
                Document.objects.update_or_create(id=int(row[0]), type=int(row[1]), warehouse=warehouse, datetime=make_aware(row[3]), receiver=row[4])

    return HttpResponse("Documents fetched!")


def fetch_documents_items():
    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:

            cursor.execute("SELECT ob_Id, ob_TowId, ob_Ilosc, ob_DokMagId FROM d_Pozycja;")

            for row in cursor.fetchall():

                print(f"Fetching document items, id={int(row[0])}")

                product = Product.objects.get(id=int(row[1]))
                Item.objects.update_or_create(id=int(row[0]), defaults={'id': int(row[0]), 'product': product, 'amount': int(row[2])})

                doc_items = Document.objects.get(id=int(row[3])).items
                if not doc_items.filter(id=int(row[0])).exists():
                    doc_items.add(int(row[0]))

    return HttpResponse("Documents items fetched!")


def fetch_warehouses():
    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT mag_Id, mag_Symbol, mag_Nazwa FROM s_Magazyn;")
            for row in cursor.fetchall():
                Warehouse.objects.update_or_create(id=int(row[0]), defaults={'id': int(row[0]), 'symbol': row[1], 'name': row[2]})

    return HttpResponse("Warehouses fetched!")


def fetch_all_data(request):

    fetch_groups()
    fetch_features_dict()
    fetch_products()
    fetch_product_features_dependencies()
    fetch_warehouses()
    fetch_documents()
    fetch_documents_items()

    return HttpResponse("All data fetched!")
