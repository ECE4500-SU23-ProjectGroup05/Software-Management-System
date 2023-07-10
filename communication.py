import json
import utils
import asyncio
import threading
import websockets
import data_collection

from asgiref.sync import async_to_sync


class Communication:
    """
    The base communication model of the client.
    """
    mac_address, client_ip = None, None
    greeting, trigger = "PING", "DATA"

    def __init__(self, websocket_url, data=None):
        self.ws_url = websocket_url
        self.client_data = data
        self.websocket = None
        self.lock = threading.Lock()
        self.send = False

    async def connect_server(self, actions):
        """
        Continuously establishing connection with the server
        :param actions: an async function to execute
        :return: nothing
        """
        while True:
            try:
                async with websockets.connect('ws://127.0.0.1:8000/ws/socket-server/') as websocket:
                    print('WebSockets connection established.')

                    self.mac_address = data_collection.get_mac_addr()
                    self.client_ip = data_collection.get_router_ip()
                    self.websocket = websocket

                    # Perform any initial actions or send messages after the connection is established.
                    await websocket.send(json.dumps(
                        {
                            "mac_address": self.mac_address,
                            "client_ip": self.client_ip,
                            "message": self.greeting,
                        },
                    ))

                    # Perform any subsequent actions after connection.
                    await actions()

            except websockets.ConnectionClosedError:
                print('Connection closed. Reconnecting in 5 seconds...')
                await asyncio.sleep(5)

            except ConnectionRefusedError:
                print('Connection Refused. Reconnecting in 15 seconds...')
                await asyncio.sleep(15)

    async def timed_communication(self, break_time=2.5e-3):
        """
        Send messages to the server (connected through websocket)
        at continuous intervals (break time)
        :param break_time: the break time (in hours)
        :return: nothing
        """
        self._test_connection()
        while True:
            await self._send_software_info()
            utils.sleep_for_some_time(break_time)

    async def receive_and_react(self):
        """
        Receive, process, and respond to the messages from the server at once
        :return: nothing
        """
        self._test_connection()
        while True:
            message = await self.websocket.recv()
            print('Received message from server:', message)

            # Perform the client-side logic based on server events
            if message == self.trigger:
                # Send the data back to the server
                await self._send_software_info()

            # Perform any other client-side logic based on server events
            pass

    def _communication_timer(self, break_time):
        utils.sleep_for_some_time(break_time)
        self.send = True

    async def bidirectional_communication(self):
        """
        Perform the bidirectional communication logic with the server,
        including both timed_communication and receive_and_react.
        :return: nothing
        """
        thread1 = threading.Thread(
            target=async_to_sync(self.receive_and_react),
            args=(),
            daemon=True,
        )
        thread2 = threading.Thread(
            target=async_to_sync(self.timed_communication),
            args=(),
            daemon=True,
        )

        thread1.start()
        thread2.start()

    def _test_connection(self):
        if self.websocket is None:
            raise Exception("ERROR: You have not established a connection to the sever!")

    async def _send_software_info(self):
        """
        Send a message about all installed software to the connected server
        :return: nothing
        """
        # Lock the thread
        self.lock.acquire()

        # Communicate if not blocked
        data = data_collection.get_installed_software()

        # If it is the first time to send the data
        if self.client_data is None:
            await self.websocket.send(json.dumps({
                "status": "update",  # "status": "new"
                "time": utils.get_current_time(),
                "installed": data,
                "uninstalled": {},
            }))
            print('New Data has been sent to server.')
            self.client_data = data

        # If it is not the first time and there's a change
        elif self.client_data != data:
            installed = set(data.keys()) - set(self.client_data.keys())
            uninstall = set(self.client_data.keys()) - set(data.keys())
            await self.websocket.send(json.dumps({
                "status": "update",
                "time": utils.get_current_time(),
                "installed": {key: data[key] for key in installed},
                "uninstalled": {key: self.client_data[key] for key in uninstall},
            }))
            print('The updated data has been sent to server.')
            self.client_data = data

        # Release the lock
        self.lock.release()

    async def default_action(self, **kwargs):
        pass
