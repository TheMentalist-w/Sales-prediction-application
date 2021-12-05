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


class ProductPrediction(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    prediction = models.ForeignKey('Prediction', on_delete=models.DO_NOTHING)


class Prediction(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    value = models.IntegerField()


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    symbol = models.CharField(max_length=64)
    name = models.CharField(max_length=256)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    inventory = models.IntegerField()
    features = models.ManyToManyField(Feature, through=ProductFeature)
    predictions = models.ManyToManyField(Prediction, through=ProductPrediction)
    is_archived = models.BooleanField(default=False)


class Place(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    population = models.IntegerField()
    avg_salary = models.FloatField()


class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    amount = models.IntegerField()


class Document(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.IntegerField()
    place = models.ForeignKey(Place, default=None, on_delete=models.DO_NOTHING)
    datetime = models.DateTimeField(blank=True)
    items = models.ManyToManyField(Item, default=None)
