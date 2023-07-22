from django.contrib import admin
from .models import WhiteList, UnauthorizedApp
from import_export.admin import ExportActionModelAdmin
from import_export.formats import base_formats
from .resources import UnauthorizedAppResource, WhiteListResource
from .utils import tools


# Register your models here.
class UnauthorizedAppAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    formats = [base_formats.CSV]
    resource_class = UnauthorizedAppResource
    search_fields = ['app_name', 'ip_addr']
    list_display = ['ip_addr', 'app_name']
    actions = ['update_database']

    def has_add_permission(self, request):
        return False

    @admin.action(description="update unauthorized app list")
    def update_database(self, request, queryset):
        tools.read_black_white_list()


class WhiteListAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    formats = [base_formats.CSV]
    resource_class = WhiteListResource
    search_fields = ['app_name', 'ip_addr']
    list_display = ['ip_addr', 'app_name']
    actions = ['update_database']

    @admin.action(description="update unauthorized app list")
    def update_database(self, request, queryset):
        tools.read_black_white_list()


admin.site.register(WhiteList, WhiteListAdmin)
admin.site.register(UnauthorizedApp, UnauthorizedAppAdmin)
