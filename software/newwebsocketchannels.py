import asyncio
import cv2
import numpy as np
import websockets
import json
import time
import keyboard  # Make sure to install this module

async def receive_video_stream():
    while True:
        try:
            async with websockets.connect("ws://10.9.0.125:8001") as websocket:
                print("Connected to video streaming endpoint")
                while True:
                    frame_data = await websocket.recv()

                    # Convert frame data to numpy array
                    frame = np.frombuffer(frame_data, dtype=np.uint8)

                    # Decode frame as an image
                    image = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                    # Display the received frame
                    cv2.imshow('Received Frame', image)
                    cv2.waitKey(1)  # Adjust the delay as needed

                    # Check for keyboard commands
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        except Exception as e:
            print(f"Error: {e}")
            print("Attempting to reconnect...")
            await asyncio.sleep(3)  # Wait for 3 seconds before attempting to reconnect

async def send_commands():
    async def send_messages(websocket):
        while True:
            try:
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

                await asyncio.sleep(0.4)  # Adjust the delay time as needed
                

            except Exception as e:
                print(f"Error: {e}")
                print("Attempting to reconnect...")
                await asyncio.sleep(3)  # Wait for 3 seconds before attempting to reconnect

    while True:
        try:
            async with websockets.connect("ws://10.9.0.125:8000") as websocket:
                print("Connected to WebSocket server")
                await send_messages(websocket)
        except Exception as e:
            print(f"Error: {e}")
            print("Attempting to reconnect...")
            await asyncio.sleep(3)  # Wait for 3 seconds before attempting to reconnect                         

async def main():
    task1 = asyncio.create_task(receive_video_stream())
    task2 = asyncio.create_task(send_commands())
    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    asyncio.run(main())