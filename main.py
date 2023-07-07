import asyncio
import communication

communicator = communication.Communication()

asyncio.get_event_loop().run_until_complete(
    communicator.connect_server(communicator.timed_communication)
)
