from import_export import resources
from .models import UnauthorizedApp

class UnauthorizedAppResource(resources.ModelResource):
    class Meta:
        model = UnauthorizedApp
        fields = ('id','app_name','reason','ip_addr','install_date')
