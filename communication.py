import json
import utils
import asyncio
import websockets
import data_collection


class Communication:
    """
    The base communication model of the client.
    """
    mac_address = data_collection.get_mac_addr()
    client_ip = data_collection.get_router_ip()
    greeting, trigger = "PING", "DATA"
    client_data = None

    async def connect_server(self, actions):
        """
        Continuously establishing connection with the server
        :param actions: an async function that takes the return object of
        `websocket.connect()` as the parameter
        :return: nothing
        """
        while True:
            try:
                async with websockets.connect('ws://127.0.0.1:8000/ws/socket-server/') as websocket:
                    print('WebSockets connection established.')

                    # Perform any initial actions or send messages after the connection is established.
                    await websocket.send(json.dumps(
                        {
                            "mac_address": self.mac_address,
                            "client_ip": self.client_ip,
                            "message": self.greeting,
                        },
                    ))

                    # Perform any subsequent actions after connection.
                    await actions(websocket)

            except websockets.ConnectionClosedError:
                print('Connection closed. Reconnecting in 5 seconds...')
                await asyncio.sleep(5)

            except ConnectionRefusedError:
                print('Connection Refused. Reconnecting in 15 seconds...')
                await asyncio.sleep(15)

    async def timed_communication(self, websocket, break_time=72):
        """
        Receive and process messages from the server at continuous intervals
        :param websocket: the return object of `websocket.connect()`
        :param break_time: the break time (in hours)
        :return: nothing
        """
        while True:
            message = await websocket.recv()
            print('Received message from server:', message)

            # Send data back to the server if needed
            condition = True if message == self.trigger else False

            # Process the received message and perform client-side logic accordingly
            if condition is True:
                data = data_collection.get_installed_software()

                if self.client_data is None:
                    await websocket.send(json.dumps({
                        "status": "new",
                        "data": data,
                    }))
                    print('New Data has been sent to server.')
                    self.client_data = data
                elif self.client_data != data:
                    await websocket.send(json.dumps({
                        "status": "update",
                        "data": data,
                    }))
                    print('The updated data has been sent to server.')
                    self.client_data = data

                await websocket.close()
                utils.sleep_for_some_time(break_time)
                break

            # Perform any other client-side logic based on server events
            pass

    async def default_action(self, **kwargs):
        pass
