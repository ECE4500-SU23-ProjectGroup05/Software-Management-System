from import_export import resources
from .models import UnauthorizedApp, WhiteList


class UnauthorizedAppResource(resources.ModelResource):
    class Meta:
        model = UnauthorizedApp
        fields = ('id', 'app_name', 'reason', 'ip_addr', 'install_date')


class WhiteListResource(resources.ModelResource):
    class Meta:
        model = WhiteList
        fields = ('id', 'app_name', 'version', 'ip_addr')
