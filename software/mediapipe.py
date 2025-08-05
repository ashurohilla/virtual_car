import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector
from picamera2 import Picamera2
from gpiozero import Button,LED,Servo
MOTOR_A_IN1 = LED(15)
MOTOR_A_EN = LED(23)
# Servo control pin
servo = Servo(14)
val = 0.5
def map_servo_value(x):
    # Map the x-value from the range [0, 500] to the range [-1, 1]
    mapped_value = (x / 250) - 1
    # Clamp the mapped value within the range [-1, 1]
    mapped_value = max(1, min(mapped_value, -1))
    # Round the mapped value to two decimal points
    return round(mapped_value, 2)
def controlmotor(h):
    x=2 
    if h > 120:
        # Stop the motor
        MOTOR_A_IN1.off()
        print("motor stoped")
    else:
        # Run the motor
        print("running motor")
        MOTOR_A_IN1.on()
        MOTOR_A_EN.off() # You may need to adjust this based on your motor setup
    


    return x

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640,480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
detector = FaceDetector(minDetectionCon=0.5)
list=[]
while True:
    im= picam2.capture_array()
    im, bboxs= detector.findFaces(im,draw=True)
    if bboxs:
        bbox = bboxs[0]["bbox"]
        # bboxInfo - "id","bbox","score","center"
        center = bboxs[0]["center"]
        cv2.circle(im, center, 5, (255, 0, 255), cv2.FILLED)
        x, y, w, h = bbox
        cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw a rectangle around the face
        center = bboxs[0]["center"] 
        # print(x,y,w,h)
        servo_angle = map_servo_value(x)
        servo.value = servo_angle
        # print(servo_angle)
        print(h)
        motor = controlmotor(h)
    else:
        servo.value=0
        MOTOR_A_IN1.off()
        print("motor stoped")    
       
    cv2.imshow("image",im)
    key = cv2.waitKey(1)
    if key == 27:  # esc
         break
cv2.destroyAllWindows()    