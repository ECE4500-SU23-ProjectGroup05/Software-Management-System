import json
import websockets
import data_collection


async def connect():
    async with websockets.connect('ws://127.0.0.1:8000/ws/socket-server/') as websocket:
        print('WebSocket connection established.')

        # Perform any initial actions or send messages after the connection is established.
        await websocket.send('PING')
        # await websocket.send(json.dumps(
        #     {
        #         "client": "client_id",
        #         "message": "PING",
        #         "IP": "client_ip",
        #     },
        # ))

        # Continuously receive and process messages from the server
        while True:
            message = await websocket.recv()
            print('Received message from server:', message)

            # Send data back to the server if needed
            condition = True if message == 'DATA' else False

            # Process the received message and perform client-side logic accordingly
            if condition is True:
                data = data_collection.get_installed_software()
                await websocket.send(json.dumps(data))
                # await websocket.send('Some data to send back to the server')
                print('Data has been sent to server.')

            # Perform any other client-side logic based on server events
