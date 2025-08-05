import asyncio
import websockets
from gpiozero import Button,LED,Servo

import time
import json

# Motor control pins
MOTOR_A_IN1 = LED(15)
MOTOR_A_EN = LED(23)

# Servo control pin
servo = Servo(14)
val = 0.5


# Set up GPIO pins

# Motor control function

    
# Servo control function

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
            if motor_command == 'forward':
                print("going forward")
                MOTOR_A_IN1.on()
                MOTOR_A_EN.on()
                
            elif motor_command == 'backward':
                MOTOR_A_IN1.on()
                MOTOR_A_EN.off()
                print("going backward")

            elif motor_command == 'stop':
                print("going stop")
                MOTOR_A_IN1.off()
            else:
                print(f"Unknown motor command: {motor_command}")
                print("motor are stoped")

            # Control the servo based on the received command
            if servo_command == 'left':
                servo.value = -1
            elif servo_command == 'right':
                servo.value = 1
            elif servo_command== 'center':
                servo.value = 0 
            else:
                print(f"Unknown servo command: {servo_command}")

            await websocket.send(f"Server received: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")

start_server = websockets.serve(handle_websocket, "0.0.0.0", 8000)

print("WebSocket server started")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()