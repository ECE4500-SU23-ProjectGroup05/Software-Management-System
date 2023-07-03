import json

from channels.generic.websocket import AsyncWebsocketConsumer
from MyServer.my_logic import compare_all, OFFICIAL_DATA, RESULT_DATA


class MyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Perform connection setup here
        await self.accept()
        await self.send(json.dumps(
            {
                "message": "PING, a connection has established!",
            },
        ))

    async def disconnect(self, close_code):
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
                await self.send('DATA')
            else:
                result = compare_all(parsed_data, OFFICIAL_DATA)
                RESULT_DATA.append(result)
                print(result)

        except json.JSONDecodeError:
            print("The received client data is not in a valid JSON format.")
