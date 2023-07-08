from django.contrib import admin
from .models import WhiteList, UnauthorizedApp

# Register your models here.

# TODO: Delete UnauthorizedApp after test

admin.site.register(WhiteList)
admin.site.register(UnauthorizedApp)
