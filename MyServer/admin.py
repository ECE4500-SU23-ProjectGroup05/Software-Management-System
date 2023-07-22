from django.contrib import admin
from .models import WhiteList, UnauthorizedApp
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export.formats import base_formats
from .resources import UnauthorizedAppResource
# Register your models here.

class UnauthorizedAppAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    formats = [base_formats.CSV]
    resource_class = UnauthorizedAppResource
    search_fields = ['app_name','ip_addr']


admin.site.register(WhiteList)
admin.site.register(UnauthorizedApp, UnauthorizedAppAdmin)
