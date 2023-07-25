import os
import csv
import time
import datetime
import threading
import ipaddress

from .models import WhiteList, UnauthorizedApp
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

from server_side.settings import BASE_DIR
from channels.layers import get_channel_layer
from MyEmail.email_sending import send_email, email_interval

# Global variable that stores the black and white list.
OFFICIAL_DATA = {}
CLIENTS_ID = set()


class MyTools:
    """
    The tool box for the server side logic.
    """

    @staticmethod
    def read_black_white_list():
        """
        This method reads the white list from the database
        and transform it into a dict format
        :return: data in a dict format
        """
        file_path = os.path.join(BASE_DIR, 'MyServer', 'test.csv')

        # Data format of the given OFFICIAL_DATA.
        data = {
                   "version": {"1.0.1", "1.0.2"},  # 'any' means all versions
                   "IP_addr": {"195.0.0.1", "195.0.0.2"},  # 0.0.0.0 means all IP address
               },

        # Replace app_name with real application's name (e.g. Macfee)
        official_data_format = {"app_name1": data, "app_name2": data}

        white_list = WhiteList.objects.raw("select * from MyServer_whitelist")

        white_list_name = [row.app_name for row in white_list]
        authorized_app = UnauthorizedApp.objects.filter(reason='authorized')

        for row in authorized_app:
            if row.app_name not in white_list_name:
                UnauthorizedApp.objects.filter(app_name=row.app_name).update(reason='unauthorized')
            else:
                app_white_list = WhiteList.objects.filter(app_name=row.app_name)
                white_list_ip = [row.ip_addr for row in app_white_list]
                if (row.ip_addr not in white_list_ip) and ("0.0.0.0" not in white_list_ip):
                    UnauthorizedApp.objects.filter(app_name=row.app_name, ip_addr=row.ip_addr).update(
                        reason='unauthorized')

        for row in white_list:
            if row.ip_addr == "0.0.0.0":
                UnauthorizedApp.objects.filter(app_name=row.app_name).update(reason='authorized')
            else:
                UnauthorizedApp.objects.filter(app_name=row.app_name, ip_addr=row.ip_addr).update(reason='authorized')
            if row.app_name in OFFICIAL_DATA:
                OFFICIAL_DATA[row.app_name]["version"].add(row.version)
                OFFICIAL_DATA[row.app_name]["IP_addr"].add(row.ip_addr)
            else:
                OFFICIAL_DATA[row.app_name] = {
                    "version": set(row.version),
                    "IP_addr": set(row.ip_addr)
                }
        return OFFICIAL_DATA

    @staticmethod
    def compare_all(client_data, client_ip, official_data=None):
        """
        This method compare the client_data with the official list according
        to its ip_address
        :return: unauthorized software name and its data in a dict format
        """

        if official_data is None:
            official_data = OFFICIAL_DATA
        # TODO: Complete the compare logic.
        data = {
            "version": "1.0.1",
            "Install_date": "20010101",
        }
        client_data_format = {"app_name1": data, "app_name2": data}
        client_ip_format = "195.0.0.1"
        result = {}

        for app_name, app_data in client_data.items():
            if app_name in official_data:
                if ("0.0.0.0" in official_data[app_name]['IP_addr']) or (
                        client_ip in official_data[app_name]['IP_addr']):
                    if ('any' in official_data[app_name]['version']) or (
                            app_data['version'] in official_data[app_name]['version']):
                        continue
            result[app_name] = app_data

        return result

    @staticmethod
    def query_ip(input_IP):
        """
        This method returns the result information for a given IP (with input
        format: e.g., '192.0', '192.168.0.212') in the database
        :return: all unauthorized apps where ip_addr starts with the given IP
        """
        param = [input_IP + "%%"]
        result = UnauthorizedApp.objects.raw("select * from MyServer_unauthorizedapp where ip_addr like %s", param)
        result_dict = [model_to_dict(data) for data in result]
        return result_dict

    @staticmethod
    def query_ip_with_mask(input_IP):
        """
        This method returns the result information for a given IP (with input
        format: e.g., '192.168.0.32/27') in the database
        :return: all unauthorized apps and info within the given IP range
        """
        ip_net = ipaddress.ip_network(input_IP, strict=False)
        start_ip = int(ip_net.network_address)
        end_ip = int(ip_net.broadcast_address)
        result = []
        all_data = UnauthorizedApp.objects.raw("select * from MyServer_unauthorizedapp")
        for data in all_data:
            ip_addr_num = int(ipaddress.ip_network(data.ip_addr).network_address)
            if end_ip >= ip_addr_num >= start_ip:
                data_dict = model_to_dict(data)
                result.append(data_dict)
        return result

    @staticmethod
    def export_query_result(data, filename):
        """
        The method reads the data of the comparison results from the database
        and exports the results as a local CSV file
        :param data: the result in a list of dict
        :param filename: the name of the CSV file
        :return: nothing
        """
        if len(data) == 0:
            print("NOTICE: No clients on this IP.")
            return

        keys = data[0].keys() if data else []
        filename = filename.replace('/', '~') + ".csv"

        with open(filename, 'w', newline='', encoding='gbk', errors='replace') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()

            for row in data:
                writer.writerow(row)

    @staticmethod
    def send_message_to_group(group_name, message='DATA'):
        """
        Send a message to the specific group
        :param group_name: the group to send
        :param message: the message to send, can be a dict
        :return: nothing
        """
        channel_layer = get_channel_layer()
        # TODO: fix the potential bugs here
        channel_layer.group_send(
            group_name, {
                'type': 'web.message',
                'message': message
            }
        )

    @staticmethod
    def send_email_to_user(filename, data=None):
        """
        Send an email attached with one file to all users
        CAUTION: DO NOT INCLUDE INVALID CHAR IN THE FILENAME
        :param filename: the filename without '.csv', etc.
        :param data: the specialized data in the dict form of
             {
                "unauthorized": value,
                "key": value
             }
        :return: nothing
        """
        csv_name = filename.replace('/', '~') + ".csv"
        users = User.objects.all()

        for user in users:
            user_email = user.email
            send_email(receiver=user_email, csv_name=csv_name, data=data)

    @staticmethod
    def timestamp_to_date(timestamp):
        # Convert the timestamp to a datetime object
        dt_object = datetime.datetime.fromtimestamp(timestamp)

        # Format the datetime object to a desired date format
        formatted_date = dt_object.strftime('%Y-%m-%d')  # Change the format

        return formatted_date

    @staticmethod
    def _send_timed_email_notification():
        """
        Send timed email notification to all admin users. You can change for
        different timed intervals in the settings.yml in MyEmail folder
        :return: nothing
        """
        if email_interval == -1:
            return

        IPv4_addr = "0.0.0.0/0"

        while True:
            time.sleep(30)
            data = tools.query_ip_with_mask(IPv4_addr)
            tools.export_query_result(data, IPv4_addr)

            # TODO: complete the following feature if possible
            # Include number of app on the black list, not on list, etc.
            # message box: e.g., 3 new apps has been installed since last time
            # message box: The client has installed an app on the black list, etc.

            specialized_info = {"unauthorized": len(data)}
            tools.send_email_to_user(IPv4_addr, specialized_info)
            time.sleep(email_interval * 24 * 3600 - 30)

    @staticmethod
    def start_timed_email_notification():
        thread = threading.Thread(
            target=tools._send_timed_email_notification, args=(), daemon=True,
        )
        thread.start()


tools = MyTools()

tools.read_black_white_list()
tools.start_timed_email_notification()
