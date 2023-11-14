'''
Database Models
'''

from django.db import models  # noqa
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    '''manager for user'''

    def create_user(self, email, password=None, **extra_field):
        ''' create, save, return new user'''

        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self.db)

        return user

class User(AbstractBaseUser,PermissionsMixin):
    '''user in system'''

    email=models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    object = UserManager()

    USERNAME_FIELD = 'email'
