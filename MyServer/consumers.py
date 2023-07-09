import json

from channels.generic.websocket import AsyncWebsocketConsumer

from MyServer.my_logic import OFFICIAL_DATA, CLIENTS_ID, \
    read_black_white_list, query_ip, query_ip_with_mask, \
    export_query_result, send_message_to_group, compare_all
from .models import UnauthorizedApp


class MyConsumer(AsyncWebsocketConsumer):
    client_ip = ""
    client_mac = ""

    async def connect(self):
        # Perform connection setup here
        await self.accept()
        # Add this consumer to a specific group
        await self.channel_layer.group_add(group='clients',
                                           channel=self.channel_name)
        await self.send(json.dumps(
            {
                "message": "PING, a ws connection has established!",
            },
        ))

    async def disconnect(self, close_code):
        # Remove the consumer from the group
        await self.channel_layer.group_discard('clients', self.channel_name)
        # Perform disconnection cleanup here
        print("NOTICE: A client is disconnected from the server.")
        CLIENTS_ID.discard(self.client_mac)
        pass

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        """
        Called when our server receive something.
        """
        # Handle incoming messages from the client
        try:
            parsed_data = json.loads(text_data)
            if "message" in parsed_data and parsed_data["message"] == 'PING':
                print("Receive the greeting message from a client.")
                await self.send('PONG and you sent: ' + text_data)
                self.client_mac = parsed_data["mac_address"]
                self.client_ip = parsed_data["client_ip"]
                CLIENTS_ID.add(self.client_mac)
                await self.send('DATA')
            else:
                if parsed_data["status"] == "update":
                    new_client_app = {}
                    for app_name, app_data in parsed_data["installed"].items():
                        client_data = {
                            'version': app_data['Version'],
                            'Install_date': app_data['Install date']
                        }
                        new_client_app[app_name] = client_data
                    read_black_white_list()
                    result = compare_all(new_client_app, self.client_ip, OFFICIAL_DATA)

                    # store compare result
                    for new_app_name, new_app_data in result.items():
                        new_row = UnauthorizedApp(app_name=new_app_name, reason="unauthorized",
                                                  ip_addr=self.client_ip,
                                                  install_date=new_app_data["Install_date"])
                        new_row.save()
                    # delete uninstall app
                    for del_app_name in parsed_data["uninstalled"]:
                        UnauthorizedApp.objects.filter(app_name=del_app_name, ip_addr=self.client_ip).delete()

                    print(result)
                    print("Notice: Comparison results has printed.")

        except json.JSONDecodeError:
            print("The received client data is not in a valid JSON format.")

    async def web_message(self, event):
        message = event.get('message')
        await self.send(message)


class WebConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Perform connection setup here
        await self.accept()
        print("NOTICE: A web connection has established!")
        await self.send("PING, a web connection has established!")

    async def disconnect(self, close_code):
        # Perform disconnection cleanup here
        print("NOTICE: A web client is disconnected from the server.")
        pass

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        """
        Called when our server receive something.
        """
        # Handle incoming messages from the client
        try:
            parsed_data = json.loads(text_data)
            if "message" in parsed_data:
                IPv4_addr = parsed_data["message"]
                if IPv4_addr == '0.0.0.0':
                    print("Receive a '0.0.0.0' message from a web client.")
                    await send_message_to_group('clients', 'DATA')
                    data = query_ip(IPv4_addr)
                elif '/' in IPv4_addr:
                    print("Receive an 'xx/oo' message from a web client.")
                    data = query_ip_with_mask(IPv4_addr)
                else:
                    print("Receive an IP addr message from a web client.")
                    data = query_ip(IPv4_addr)

                export_query_result(data, IPv4_addr)
                await self.send(json.dumps(data))
                print("The result has been sent to the web client.")

                # TODO: complete the following feature if possible
                # Include number of app on the black list, not on list, etc.
                # in the result data sent to the web UI.
                # message box: e.g., 3 new apps has been installed since last time
                # message box: The client has installed an app on the black list, etc.
            else:
                print("Receive a message from a web client.")
                await self.send("Invalid message format.")

        except json.JSONDecodeError:
            print("The received client data is not in a valid JSON format.")
            await self.send("Data is not in a valid JSON format.")
