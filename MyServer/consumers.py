import json

from channels.generic.websocket import AsyncWebsocketConsumer
from MyServer.my_logic import compare_all, OFFICIAL_DATA, RESULT_DATA


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
                await self.send('DATA')
            else:
                result = compare_all(parsed_data, OFFICIAL_DATA)
                RESULT_DATA.append({
                    "mac_address": self.client_mac,
                    "client_ip": self.client_ip,
                    "result": result,
                })
                print(result)

        except json.JSONDecodeError:
            print("The received client data is not in a valid JSON format.")
