from django.apps import AppConfig
#from MyServer.my_logic import read_black_white_list


class MyserverConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MyServer'

    #def ready(self):
    #   read_black_white_list()
