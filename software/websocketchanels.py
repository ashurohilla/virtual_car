import asyncio
import websockets
import keyboard
import time
import json

async def send_messages():
    while True:
        try:
            async with websockets.connect("ws://192.168.1.39:8000") as websocket:
                print("Connected to WebSocket server")
                last_press_time = 0
                delay = 0.2  # Delay in seconds between key press events
                while True:
                    message = {
                        "motor": "stop",
                        "servo": "center"
                    }

                    # Check for key presses
                    if keyboard.is_pressed('w'):
                        message["motor"] = "forward"
                    elif keyboard.is_pressed('s'):
                        message["motor"] = "backward"

                    if keyboard.is_pressed('a'):
                        message["servo"] = "left"
                    elif keyboard.is_pressed('d'):
                        message["servo"] = "right"

                    # Convert message dictionary to JSON string
                    message_json = json.dumps(message)

                    # Send the message
                    await websocket.send(message_json)

                    # Add a delay before sending the next message
                    await asyncio.sleep(0.1)  # Adjust the delay time as needed

                    current_time = time.time()
                    if current_time - last_press_time >= delay:
                        response = await websocket.recv()
                        # print(f"Received response: {response}")
                        last_press_time = current_time

        except Exception as e:
            print(f"Error: {e}")
            print("Attempting to reconnect...")
            await asyncio.sleep(5)  # Wait for 5 seconds before attempting to reconnect

def start_websocket_client():
    asyncio.run(send_messages())

if __name__ == "__main__":
    start_websocket_client()
