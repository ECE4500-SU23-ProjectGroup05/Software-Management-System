import os
import csv
import json

from server_side.settings import BASE_DIR
from channels.layers import get_channel_layer

# Global variable that stores the black and white list.
OFFICIAL_DATA = []
RESULT_DATA = []


# Suggestion: build a class to handle the compare logic.

def read_black_white_list():
    """
    == TODO: Complete the method.
    This method reads the Black and White List of software.
    :return: data in a list, a dict, or a json format
    """
    file_path = os.path.join(BASE_DIR, 'MyServer', 'test.csv')

    # Open the CSV file for reading
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Modify the data as needed.
            modified_row = [item.upper() for item in row]
            OFFICIAL_DATA.append(modified_row)

    # Data format of the given OFFICIAL_DATA.
    data = {
               "software": "app",
               "version": "1.0.1",
               "attribute": "black/white",
               "exception": "IP address or device name",
           },

    return OFFICIAL_DATA


def compare_all(client_data, official_data=None):
    if official_data is None:
        official_data = OFFICIAL_DATA
    # TODO: Complete the compare logic.

    result = client_data
    return result


# Suggestion: build a class to handle the user queries.

def query_ip():
    pass


def query_ip_with_mask():
    return


def save_query_result():
    """
    Save the query result to a csv file.
    """
    pass


async def send_message_to_group(group_name, message='DATA'):
    """
    Send a message to the specific group
    :param group_name: the group to send
    :param message: the message to send, can be a dict
    :return: nothing
    """
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        group_name, {
            'type': 'web.message',
            'message': message
        }
    )
