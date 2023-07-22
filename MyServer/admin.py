from django.contrib import admin
from .models import WhiteList, UnauthorizedApp
from import_export.admin import ExportActionModelAdmin
from import_export.formats import base_formats
from .resources import UnauthorizedAppResource, WhiteListResource


# Register your models here.
class UnauthorizedAppAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    formats = [base_formats.CSV]
    resource_class = UnauthorizedAppResource
    search_fields = ['app_name', 'ip_addr']
    list_display = ['ip_addr', 'app_name', 'install_date']


class WhiteListAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    formats = [base_formats.CSV]
    resource_class = WhiteListResource
    search_fields = ['app_name', 'ip_addr']
    list_display = ['ip_addr', 'app_name']


admin.site.register(WhiteList, WhiteListAdmin)
admin.site.register(UnauthorizedApp, UnauthorizedAppAdmin)
