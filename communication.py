import json
import time
import utils
import queue
import threading
import websocket
import data_collection


class Communication:
    """
    The base communication model of the client.
    """
    mac_address, client_ip = None, None
    greeting, trigger = "PING", "DATA"

    def __init__(self, websocket_url, break_time=2.5e-3):
        """
        The constructor of the class Communication
        :param websocket_url: The url used to establish websocket connection
        :param break_time: the break time (in hours)
        """
        self.exception_q = queue.Queue()
        self.lock = threading.Lock()
        self.ws_url = websocket_url
        self.time = break_time
        self.client_data = None
        self.websocket = None
        self.running = True
        if not break_time > 0 and break_time is not -1:
            print("CAUTION: You set an invalid negative update interval.")
            print("         The timed communication is thus disabled.")
            self.time = -1
        if 0 <= break_time < 1:
            print("CAUTION: You set a frequent update interval.")
            print("SUGGEST: Please change it in the settings.")

    def connect_server(self, actions, rc_time=15):
        """
        Continuously establishing connection with the server
        :param actions: a function to execute
        :param rc_time: interval to reconnect to the server if disconnected
        :return: nothing
        """
        while True:
            try:
                ws = websocket.create_connection(self.ws_url)
                print('WebSockets connection established.')

                self.mac_address = data_collection.get_mac_addr()
                self.client_ip = data_collection.get_router_ip()
                self.websocket = ws

                # Perform any initial actions or send messages after the connection is established.
                self.websocket.send(json.dumps(
                    {
                        "mac_address": self.mac_address,
                        "client_ip": self.client_ip,
                        "message": self.greeting,
                    },
                ))

                # Perform any subsequent actions after connection.
                actions()

            except ConnectionResetError:
                print('Connection Reset. Reconnecting in ' + str(rc_time) + ' seconds...')
                self.running = True
                time.sleep(rc_time)

            except ConnectionRefusedError:
                print('Connection Refused. Reconnecting in ' + str(rc_time) + ' seconds...')
                self.running = True
                time.sleep(rc_time)

    def timed_communication(self):
        """
        Send messages to the server (connected through websocket)
        at continuous intervals (break time)
        :return: nothing
        """
        self._test_connection()
        if self.time == -1:
            print("CAUTION: You have disabled the timed communication function "
                  "in the settings.")
            print("         You have to manually check for update on server "
                  "as a result.")
            return
        while self.running:
            self._send_software_info()
            utils.sleep_for_some_time(self.time)

    def _timed_communication_thread(self):
        """
        Run timed_communication() and throw the exception to the
        class-level queue
        :param
        :return: nothing
        """
        try:
            self.timed_communication()
        except Exception as e:
            self.lock.acquire()
            self.running = False
            self.exception_q.put([e, "timed_communication"])
            self.lock.release()

    def receive_and_react(self):
        """
        Receive, process, and respond to the messages from the server at once
        :return: nothing
        """
        self._test_connection()
        while self.running:
            message = self.websocket.recv()
            print('Received message from server:', message)

            # Perform the client-side logic based on server events
            if message == self.trigger:
                # Send the data back to the server
                self._send_software_info()

            # Perform any other client-side logic based on server events
            pass

    def _receive_and_react_thread(self):
        """
        Run receive_and_react() and throw the exception to the
        class-level queue
        :return: nothing
        """
        try:
            self.receive_and_react()
        except Exception as e:
            self.lock.acquire()
            self.running = False
            self.exception_q.put([e, "receive_and_react"])
            self.lock.release()

    def bidirectional_communication(self):
        """
        Perform the bidirectional communication logic with the server,
        including both timed_communication and receive_and_react.
        :return: nothing
        """
        thread1 = threading.Thread(
            target=self._timed_communication_thread,
            args=(),
            daemon=True,
        )
        thread2 = threading.Thread(
            target=self._receive_and_react_thread,
            args=(),
            daemon=True,
        )
        thread1.start(), thread2.start()

        while True:
            try:
                # Get the exception from the queue
                exception = self.exception_q.get(block=False)
                print(f"Exception occurred in {exception[1]} thread: {exception[0]}")
                # Terminate the thread cleanly
                thread1.join(), thread2.join()
                # Raise the exception to self.connect_server method
                raise exception[0]
            except queue.Empty:
                # Continue with other tasks if no exception
                time.sleep(1)

    def _test_connection(self):
        if self.websocket is None:
            raise Exception("ERROR: You have not established a connection to the sever!")

    def _send_software_info(self):
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
            self.websocket.send(json.dumps({
                "status": "new",
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
            self.websocket.send(json.dumps({
                "status": "update",
                "time": utils.get_current_time(),
                "installed": {key: data[key] for key in installed},
                "uninstalled": {key: self.client_data[key] for key in uninstall},
            }))
            print('The updated data has been sent to server.')
            self.client_data = data

        # Release the lock
        self.lock.release()

    def default_action(self, **kwargs):
        pass
