from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class UserManager(BaseUserManager):
    
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must provide an username!')

        user = self.model(
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, password, email = None):
        user = self.create_user(
            username = username,
        )

        user.is_superuser = True   # @TODO is_superuser, is_staff or both?
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
    