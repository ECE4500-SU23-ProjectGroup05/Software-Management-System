import os
import csv
import json

from .models import WhiteList, UnauthorizedApp 

from server_side.settings import BASE_DIR
from channels.layers import get_channel_layer

# Global variable that stores the black and white list.
OFFICIAL_DATA = {}
RESULT_DATA = []


# Suggestion: build a class to handle the compare logic.

def read_black_white_list():
    """
    This method reads the white list from the database
    and transform it into a dict format
    :return: data in a dict format
    """
    file_path = os.path.join(BASE_DIR, 'MyServer', 'test.csv')
    

    # Data format of the given OFFICIAL_DATA.
    data = {
               "version": set(["1.0.1","1.0.2"]), # 'any' means all versions
               "IP_addr": set(["195.0.0.1","195.0.0.2"]),# 0.0.0.0 means all IP address
           },
    
    # Replace app_name with real application's name (e.g. Macfee)
    official_data_format = { "app_name1": data,"app_name2": data}

    white_list = WhiteList.obejcts.raw("select * from MyServer_whitelist")
    for row in white_list:
        if row.app_name in OFFICIAL_DATA:
            OFFICIAL_DATA[row.app_name]["version"].add(row.version)
            OFFICIAL_DATA[row.app_name]["IP_addr"].add(row.ip_addr)
        else:
            OFFICIAL_DATA[row.app_name] = {
                "version": set(row.version),
                "IP_addr": set(row.ip_addr)
                }
    return OFFICIAL_DATA


def compare_all(client_data,client_ip,official_data=None):
    """
    This method compare the client_data with the official list according
    to its ip_address
    :return: unauthorize software name and its data in a dict format
    """
    
    if official_data is None:
        official_data = OFFICIAL_DATA
    # TODO: Complete the compare logic.
    data = {
               "version": "1.0.1",
               "Install_date": "20010101",
           }
    client_data_format = {"app_name1":data, "app_name2": data}
    client_ip_format = "195.0.0.1"
    result = {}
    
    # TODO: Replace the format with real data when client_data is
    #       in the correct format
    for app_name, app_data in client_data_format.items():
        if app_name in official_data:
            if ("0.0.0.0" in official_data[app_name]['IP_addr']) or (client_ip_format in official_data[app_name]['IP_addr']):
                if ('any' in official_data[app_name]['version']) or (app_data['version'] in official_data[app_name]['version']):
                    continue
        result[app_name] = app_data
    
    return result


def query_ip(input_IP):
    """
    This method returns the result information for a given IP (with input 
    format: e.g., '192.0', '192.168.0.212') in the database
    :return: all unauthorized apps where ip_addr starts with the given IP
    """
    param = [input_IP+"%%"]
    result = UnauthorizedApp.objects.raw("select * from MyServer_unauthorizedapp where ip_addr like %s",param)
    return result


def query_ip_with_mask(input_IP):
    """
    This method returns the result information for a given IP (with input 
    format: e.g., '192.168.0.32/27') in the database
    :return: all unauthorized apps and info within the given IP range
    """
    pass
  
  
def export_query_result():
    """
    The method reads the data of the comparison results from the database
    and exports the results as a local CSV file
    """
    pass
