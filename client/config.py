import os
import sys
import time
import yaml


def read_settings():
    # Running from PyInstaller bundle
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    else:  # Running from source code
        app_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(app_path, "settings.yml")

    try:
        with open(filepath) as fin:
            settings = yaml.load(fin, Loader=yaml.FullLoader)

    except FileNotFoundError as error:
        print(error)
        raise error

    return settings
