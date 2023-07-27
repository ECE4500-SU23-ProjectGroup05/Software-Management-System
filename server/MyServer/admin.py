from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from admin_extra_buttons.api import ExtraButtonsMixin, button
from import_export.admin import ExportActionModelAdmin, ImportExportActionModelAdmin, ImportMixin
from import_export.formats import base_formats
from .models import WhiteList, UnauthorizedApp
from .resources import UnauthorizedAppResource, WhiteListResource
from .utils import tools


# Register your models here.
class UnauthorizedAppAdmin(ExportActionModelAdmin, ExtraButtonsMixin, admin.ModelAdmin):
    to_encoding = 'GB18030'  # encoding of export to csv
    formats = [base_formats.CSV]
    actions = ['update_database']
    resource_class = UnauthorizedAppResource

    search_fields = ['app_name', 'ip_addr']
    list_display = ['ip_addr', 'app_name']
    list_filter = ['ip_addr', 'app_name']
    list_per_page = 50

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(reason='unauthorized')

    def has_add_permission(self, request):
        return False

    @admin.action(description="Update selected unauthorized apps")
    def update_database(self, request, queryset):
        tools.read_black_white_list()

    @button()
    def check_update(self, request):
        tools.send_message_to_group('clients', 'DATA')  # send update signal to clients
        print("Notice: The update signal has been sent to all clients.")


class WhiteListAdmin(ImportExportActionModelAdmin, ImportMixin, admin.ModelAdmin):
    to_encoding = 'GB18030'  # encoding of export to csv
    formats = [base_formats.CSV]
    actions = ['update_database']
    resource_class = WhiteListResource

    search_fields = ['app_name', 'ip_addr']
    list_display = ['ip_addr', 'app_name']
    list_filter = ['ip_addr', 'app_name']
    list_per_page = 50

    @admin.action(description="Update unauthorized lists")
    def update_database(self, request, queryset):
        tools.read_black_white_list()


admin.site.register(WhiteList, WhiteListAdmin)
admin.site.register(UnauthorizedApp, UnauthorizedAppAdmin)
