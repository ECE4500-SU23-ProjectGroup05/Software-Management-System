import os
import yaml


def read_settings():
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, "settings.yml")

    with open(filepath) as fin:
        settings = yaml.load(fin, Loader=yaml.FullLoader)

    return settings
