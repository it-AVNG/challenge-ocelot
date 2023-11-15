'''
Django admin customize
'''
from django.contrib import admin  # noqa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):
    '''define Admin pages for users'''

    ordering = ['id']
    list_display = ['email', 'name']


admin.site.register(models.User, UserAdmin)
