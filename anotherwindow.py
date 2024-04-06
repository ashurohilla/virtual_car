import sys
import threading
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import paho.mqtt.client as mqtt
import speech_recognition as sr

# MQTT Configuration
mqtt_server = "mqtt.eclipse.org"
mqtt_topic_control = "car/control"

# Function to handle MQTT messages
def on_message(client, userdata, message):
    # Process MQTT messages here
    pass

# Function to start MQTT client
def start_mqtt_client():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(mqtt_server, 1883, 60)
    client.subscribe(mqtt_topic_control)
    client.loop_forever()

# Function to start speech recognition
def start_speech_recognition():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        # Send text to MQTT for further processing
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("IoT Car Desktop Application")
        self.setGeometry(100, 100, 800, 600)
        
        # Layout
        layout = QVBoxLayout()
        
        # Labels for each partition
        self.label1 = QLabel("MPU Gyroscope Data")
        layout.addWidget(self.label1)
        
        self.label2 = QLabel("Live Video Stream")
        layout.addWidget(self.label2)
        
        self.label3 = QLabel("Location of the Bot")
        layout.addWidget(self.label3)
        
        self.label4 = QLabel("Speech to Text")
        layout.addWidget(self.label4)
        
        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Timer for updating video stream
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video_stream)
        self.timer.start(100)  # Update every 100 milliseconds
    
    def update_video_stream(self):
        # Function to update the video stream from Raspberry Pi
        # You'll need to implement this part using OpenCV
        pass

if __name__ == "__main__":
    # Start MQTT client in a separate thread
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    # Start speech recognition in a separate thread
    speech_thread = threading.Thread(target=start_speech_recognition)
    speech_thread.daemon = True
    speech_thread.start()

    # GUI
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
