import json

from channels.generic.websocket import WebsocketConsumer
from .utils import OFFICIAL_DATA, CLIENTS_ID, tools
from .models import UnauthorizedApp
from asgiref.sync import async_to_sync


class MyConsumer(WebsocketConsumer):
    client_ip = ""
    client_mac = ""

    def connect(self):
        # Perform connection setup here
        self.accept()
        # Add this consumer to a specific group
        async_to_sync(self.channel_layer.group_add)(group='clients',
                                     channel=self.channel_name)
        self.send(json.dumps(
            {
                "message": "PING, a ws connection has established!",
            },
        ))

    def disconnect(self, close_code):
        # Remove the consumer from the group
        self.channel_layer.group_discard('clients', self.channel_name)
        # Perform disconnection cleanup here
        print("NOTICE: A client is disconnected from the server.")
        CLIENTS_ID.discard(self.client_mac)
        pass

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        """
        Called when our server receive something.
        """
        # Handle incoming messages from the client
        try:
            parsed_data = json.loads(text_data)
            if "message" in parsed_data and parsed_data["message"] == 'PING':
                print("Receive the greeting message from a client.")
                self.send('PONG and you sent: ' + text_data)
                self.client_mac = parsed_data["mac_address"]
                self.client_ip = parsed_data["client_ip"]
                CLIENTS_ID.add(self.client_mac)
                self.send('DATA')
            elif parsed_data["status"] == "update":
                print(f"Notice: Receive an update from client on {self.client_ip}")
                result = self.compare_client_info(parsed_data)
                self.store_compare_result(result, parsed_data["installed"])

                # delete uninstall app
                for del_app_name in parsed_data["uninstalled"]:
                    UnauthorizedApp.objects.filter(app_name=del_app_name,
                                                   ip_addr=self.client_ip).delete()

                print("Notice: Comparison results (update) has printed.")
            elif parsed_data['status'] == "new":
                result = self.compare_client_info(parsed_data)
                self.store_compare_result(result, parsed_data["installed"])

                print("Notice: Comparison results (new) has printed.")

        except json.JSONDecodeError:
            print("The received client data is not in a valid JSON format.")

    def compare_client_info(self, parsed_data):
        new_client_app = {}
        for app_name, app_data in parsed_data["installed"].items():
            client_data = {
                'version': app_data['Version'],
                'Install_date': app_data['Install date']
            }
            new_client_app[app_name] = client_data
        tools.read_black_white_list()
        return tools.compare_all(new_client_app, self.client_ip, OFFICIAL_DATA)

    def store_compare_result(self, result, installed_app):
        for app_name, app_data in installed_app.items():
            if app_name in result:
                database_data = UnauthorizedApp.objects.filter(app_name=app_name,
                                                               ip_addr=self.client_ip)
                if database_data.exists():
                    UnauthorizedApp.objects.filter(app_name=app_name, ip_addr=self.client_ip).update(
                        reason='unauthorized')
                else:
                    new_row = UnauthorizedApp(app_name=app_name,
                                              reason="unauthorized",
                                              ip_addr=self.client_ip,
                                              install_date=app_data["Install date"])
                    new_row.save()
            else:
                database_data = UnauthorizedApp.objects.filter(app_name=app_name,
                                                               ip_addr=self.client_ip)
                if database_data.exists():
                    UnauthorizedApp.objects.filter(app_name=app_name, ip_addr=self.client_ip).update(
                        reason='authorized')
                else:
                    new_row = UnauthorizedApp(app_name=app_name,
                                              reason="authorized",
                                              ip_addr=self.client_ip,
                                              install_date=app_data["Install date"])
                    new_row.save()

    def web_message(self, event):
        print("Update Event Triggered.")
        message = event.get('message')
        self.send(message)
        print("Update Message is Sent.")


class WebConsumer(WebsocketConsumer):

    def connect(self):
        # Perform connection setup here
        self.accept()
        print("NOTICE: A web connection has established!")

    def disconnect(self, close_code):
        # Perform disconnection cleanup here
        print("NOTICE: A web client is disconnected from the server.")
        pass

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        """
        Called when our server receive something.
        """
        # Handle incoming messages from the client
        try:
            parsed_data = json.loads(text_data)
            if "message" in parsed_data:
                IPv4_addr = parsed_data["message"]
                if '/' in IPv4_addr:
                    print("Receive an 'xx/oo' message from a web client.")
                    data = tools.query_ip_with_mask(IPv4_addr)
                else:
                    print("Receive an IP addr message from a web client.")
                    data = tools.query_ip(IPv4_addr)

                self.send(json.dumps(data, ensure_ascii=False))
                print("The result has been sent to the web client.")

            else:
                print("Receive a message from a web client.")
                self.send("Invalid message format.")

        except json.JSONDecodeError:
            print("The received client data is not in a valid JSON format.")
            self.send("Data is not in a valid JSON format.")
