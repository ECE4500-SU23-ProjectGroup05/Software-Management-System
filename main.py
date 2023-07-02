import asyncio
import communication

asyncio.get_event_loop().run_until_complete(communication.connect())
