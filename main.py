import asyncio  # Import the asyncio library for asynchronous programming
import websockets  # Import the websockets library to handle WebSocket connections
import re  # Import the re library for regular expression operations
from constants import *
from server import *

async def main(): 
    while True:
        try:
            await connect_to_twitch()
        except Exception as error:
            print(f"Error: {error}. Reconnecting now...")
            await asyncio.sleep(5)  # Waits 5 seconds before trying again

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())