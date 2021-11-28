from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class UserManager(BaseUserManager):
    
    def create_user(self, username, password=None, email=None, first_name=None, last_name=None):
        if not username:
            raise ValueError('User must provide an username!')

        user = self.model(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, password, email = None, first_name=None, last_name=None):
        user = self.create_user(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name
        )

        user.is_superuser = True  
        user.is_staff = True
        user.set_password(password)

        user.save(using=self._db)
        
        return user


class User(AbstractUser):
    
     username = models.CharField(max_length=40, unique=True)
     USERNAME_FIELD = 'username'

     def get_username(self):
        return self.username

     objects = UserManager()

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


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    symbol = models.CharField(max_length=64)
    name = models.CharField(max_length=256)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    inventory = models.IntegerField()
    features = models.ManyToManyField(Feature, through=ProductFeature)


