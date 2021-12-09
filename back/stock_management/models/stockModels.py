from django.db import models

# TODO dostosować wielkośći pól zgodnie z bazą Pitbulla


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)


class ProductFeature(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    feature = models.ForeignKey('Feature', on_delete=models.DO_NOTHING)


class Feature(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


class Place(models.Model):
    name = models.CharField(max_length=40)
    # population = models.IntegerField(default=None, blank=True)
    # avg_salary = models.FloatField(default=None, blank=True)


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    symbol = models.CharField(max_length=64)
    name = models.CharField(max_length=256)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    inventory = models.IntegerField()
    features = models.ManyToManyField(Feature, through=ProductFeature)
    is_archived = models.BooleanField(default=False)


class Prediction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField() #auto_now_add=True, blank=True
    value = models.IntegerField()
    place = models.ForeignKey(Place, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    amount = models.IntegerField()
    sign = models.IntegerField()


class Document(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.IntegerField()
    place = models.ForeignKey(Place, default=None, on_delete=models.DO_NOTHING)
    datetime = models.DateTimeField(blank=True)
    items = models.ManyToManyField(Item, default=None)
