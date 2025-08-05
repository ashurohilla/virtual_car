import asyncio
import websockets
import cv2
import numpy as np

async def receive_video_stream():
    async with websockets.connect('ws://10.13.0.248:8001') as websocket:
        print("WebSocket connected successfully")  # Print when the WebSocket connection is established

        while True:
            # Receive frame data from the server
            frame_data = await websocket.recv()
            print(frame_data)

            # Convert the received data to an image
            nparr = np.frombuffer(frame_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Display the image (You can also save it or process further)
            cv2.imshow('Video Stream', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
                break

    cv2.destroyAllWindows()

asyncio.get_event_loop().run_until_complete(receive_video_stream())