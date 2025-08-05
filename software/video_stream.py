import asyncio
import websockets
import io
import numpy as np
import cv2

async def receive_video():
    async with websockets.connect('ws://192.168.1.39:8000') as websocket:  # Adjust the URL if needed
        print("Connected to video streaming server")
        try:
            while True:
                # Receive frame data from the server
                frame_data = await websocket.recv()

                # Convert frame data to numpy array
                frame = np.frombuffer(frame_data, dtype=np.uint8)

                # Decode frame as an image
                image = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                # Display the received frame
                cv2.imshow('Received Frame', image)
                cv2.waitKey(1)  # Adjust the delay as needed

        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection to video streaming server closed: {e}")

asyncio.run(receive_video())
