import asyncio  # Import the asyncio library for asynchronous programming
import websockets  # Import the websockets library to handle WebSocket connections
import re  # Import the re library for regular expression operations
from constants import *

async def connect_to_twitch():
    try:
        async with websockets.connect(TWITCH_WS_URL) as ws:  # Connect to Twitch's WebSocket server
            print("Connected to Twitch's websocket")  # Print a message showing a successful connection

            # Append CRLF to each command
            await ws.send(f"PASS {OAUTH_TOKEN}\r\n")  # Send the OAuth token for authentication
            await ws.send(f"NICK {BOT_USERNAME}\r\n")  # Send the bot's username
            await ws.send(f"JOIN {CHANNEL}\r\n")  # Join the Twitch channel
            print(f"-> Joined {CHANNEL}")  # Print a message that the bot has joined the channel

            while True: 
                response = await ws.recv()  # Wait for message from WebSocket
                print(f"Received message: {response}")  # Log the received message

                # Responds to PING message, If Twitch gets a PONG response it'll disconnect the bot
                if "PING" in response:
                    await ws.send("PONG :tmi.twitch.tv\r\n")
                    print("-> sent PONG to Twitch")
                    continue

                match = re.search(r":(\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :(.*)", response)  # Use regex to parse message
                if match:
                    username, message = match.groups()  # Extract username and message from regex match
                    print(f"{username}: {message}")  # Print username and message

                    # If someone types !hello, mema response
                    if message.strip() == "!hello":
                        reply = f"PRIVMSG {CHANNEL} :*Your MeMa Looks at {username} with loving eyes*, Hello Sweetie!\r\n"
                        await ws.send(reply)
                        print(f"Bot: {reply}")
                        await asyncio.sleep(1)  # Add a slight delay to ensure the message is processed
    except Exception as e:
        print(f"Exception in connect_to_twitch: {e}")


