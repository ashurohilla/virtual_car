import asyncio
import websockets
from gpiozero import LED, Servo
import json
import cv2
import mediapipe as mp

# Motor control pins
MOTOR_A_IN1 = LED(15)
MOTOR_A_EN = LED(23)

# Servo control pin
servo = Servo(14)

# Initialize MediaPipe face detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Set up GPIO pins and camera
# (Assuming you have a camera connected to the Raspberry Pi)
camera = cv2.VideoCapture(0)

# Motor control function
def control_motor(direction):
    if direction == 'forward':
        MOTOR_A_IN1.on()
        MOTOR_A_EN.on()
    elif direction == 'backward':
        MOTOR_A_IN1.on()
        MOTOR_A_EN.off()
    elif direction == 'stop':
        MOTOR_A_IN1.off()
    else:
        print(f"Unknown motor command: {direction}")
        print("Motor stopped")

# Servo control function
def control_servo(position):
    if position == 'left':
        servo.value = -1
    elif position == 'right':
        servo.value = 1
    elif position == 'center':
        servo.value = 0 
    else:
        print(f"Unknown servo command: {position}")

# Function to control the servo based on the face position
def control_servo(face_center):
    # Assume the frame size is frame_width x frame_height
    frame_width = 640  # Adjust according to your camera resolution
    frame_height = 480  # Adjust according to your camera resolution
    
    # Servo center position
    servo_center = frame_width // 2
    
    # Calculate the difference between the face center and the servo center
    servo_offset = face_center[0] - servo_center
    
    # Define a threshold for servo movement
    servo_threshold = 20
    
    # If the face is within the servo threshold from the center, keep the servo centered
    if abs(servo_offset) <= servo_threshold:
        return 'center'
    # If the face is to the left of the center, move the servo left
    elif servo_offset < 0:
        return 'left'
    # If the face is to the right of the center, move the servo right
    else:
        return 'right'

# WebSocket server
async def handle_websocket(websocket, path):
    print("New client connected")
    try:
        async for message in websocket:
            # Parse the received JSON string
            data = json.loads(message)
            motor_command = data.get("motor", "")
            servo_command = data.get("servo", "")
            
            print(f"Received command - Motor: {motor_command}, Servo: {servo_command}")

            # Control the motor based on the received command
            control_motor(motor_command)

            # Control the servo based on the received command
            control_servo(servo_command)

            await websocket.send(f"Server received: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")

start_server = websockets.serve(handle_websocket, "0.0.0.0", 8000)

print("WebSocket server started")

async def main():
    async with start_server:
        while True:
            # Read frame from the camera
            ret, frame = camera.read()
            if not ret:
                print("Error reading frame")
                break

            # Get the frame width and height
            frame_height, frame_width, _ = frame.shape
            
            # Convert the image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces in the frame
            results = face_detection.process(rgb_frame)

            # If faces are detected, track them
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(frame, detection)
                    # Get the position of the face
                    bboxC = detection.location_data.relative_bounding_box
                    x, y, w, h = int(bboxC.xmin * frame_width), int(bboxC.ymin * frame_height), int(bboxC.width * frame_width), int(bboxC.height * frame_height)
                    face_center = (x + w // 2, y + h // 2)
                    
                    # Check if a person is too close to the car (within a safe distance)
                    # If too close, stop the car
                    safe_distance_threshold = 150  # Adjust according to your preference
                    if y + h >= frame_height - safe_distance_threshold:
                        control_motor('stop')
                    else:
                        # Control the servo based on the face position
                        servo_command = control_servo(face_center)
                        control_servo(servo_command)
                        # Move the car forward as long as no person is too close
                        control_motor('forward')

            # Display the frame
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

# Run the WebSocket server and face tracking loop concurrently
asyncio.gather(start_server, main())
asyncio.get_event_loop().run_forever()
