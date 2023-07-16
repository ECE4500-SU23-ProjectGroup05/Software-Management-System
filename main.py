import config
import communication

settings = config.read_settings()
websocket_url = "ws://" + str(settings["server-IP"]) + ":" + str(settings["port"]) + "/ws/socket-server/"

communicator = communication.Communication(websocket_url, settings["time"])
communicator.connect_server(communicator.bidirectional_communication, settings["reconnect"])
