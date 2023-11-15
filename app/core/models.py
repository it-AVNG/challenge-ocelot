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

    def create_user(self, email, password=None, **extra_fields):
        ''' create, save, return new user'''

        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        ''' create new super user'''

        if not email:
            raise ValueError('User must have an email address.')
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user



class User(AbstractBaseUser, PermissionsMixin):
    '''user in system'''

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
