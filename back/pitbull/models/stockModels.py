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


class Prediction(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    value = models.IntegerField()


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    symbol = models.CharField(max_length=64)
    name = models.CharField(max_length=256)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    inventory = models.IntegerField()
    features = models.ManyToManyField(Feature, through=ProductFeature)
    predictions = models.ManyToManyField(Prediction, default=None)
    is_archived = models.BooleanField(default=False)