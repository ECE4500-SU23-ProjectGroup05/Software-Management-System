from main import communicator, settings

communicator.connect_server(communicator.bidirectional_communication, settings["reconnect"])
