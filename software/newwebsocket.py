import asyncio
import websockets
import keyboard
import time

async def send_messages():
    while True:
        try:
            async with websockets.connect("ws://192.168.1.39:8000") as websocket:
                print("Connected to WebSocket server")
                last_press_time = 0
                delay = 0.2  # Delay in seconds between key press events
                while True:
                    message = ""

                    # Check for key presses
                    if keyboard.is_pressed('w'):
                        message += "forward"
                    if keyboard.is_pressed('a'):
                        if message:
                            message += ","
                        message += "left"
                    if keyboard.is_pressed('s'):
                        if message:
                            message += ","
                        message += "backward"
                    if keyboard.is_pressed('d'):
                        if message:
                            message += ","
                        message += "right"
                    if not message:
                        message = "stop"

                    current_time = time.time()
                    if current_time - last_press_time >= delay:
                        await websocket.send(message)
                        response = await websocket.recv()
                        print(f"Received response: {response}")
                        last_press_time = current_time

        except Exception as e:
            print(f"Error: {e}")
            print("Attempting to reconnect...")
            await asyncio.sleep(5)  # Wait for 5 seconds before attempting to reconnect

def start_websocket_client():
    asyncio.run(send_messages())

if __name__ == "__main__":
    start_websocket_client()
