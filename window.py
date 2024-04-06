import sys
import cv2
import speech_recognition as sr
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import geopy.distance

# MPU Gyroscope Data (Simulated for this example)
gyro_data = [0.0, 0.0, 0.0]

# Location Tracking (Simulated for this example)
start_location = (37.7749, -122.4194)  # San Francisco
current_location = start_location

# MQTT Setup
mqtt_client = mqtt.Client()
mqtt_client.connect("broker.example.com", 1883)

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture("http://raspberrypi.local:8000/stream.mjpg")
        while True:
            ret, frame = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IoT Car Control")
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QVBoxLayout()

        # MPU Gyroscope Data
        gyro_layout = QHBoxLayout()
        gyro_label = QLabel("MPU Gyroscope Data:")
        gyro_x_label = QLabel(f"X: {gyro_data[0]}")
        gyro_y_label = QLabel(f"Y: {gyro_data[1]}")
        gyro_z_label = QLabel(f"Z: {gyro_data[2]}")
        gyro_layout.addWidget(gyro_label)
        gyro_layout.addWidget(gyro_x_label)
        gyro_layout.addWidget(gyro_y_label)
        gyro_layout.addWidget(gyro_z_label)

        # Video Stream
        video_label = QLabel()
        video_thread = VideoThread()
        video_thread.change_pixmap_signal.connect(video_label.setPixmap)
        video_thread.start()

        # Location Tracking
        location_label = QLabel(f"Current Location: {current_location}")

        # Speech-to-Text
        self.speech_text = QLabel("Speech-to-Text Output:")
        self.start_speech_recognition()

        # Keyboard Input
        self.keyboard_input = QLabel("Keyboard Input:")

        main_layout.addLayout(gyro_layout)
        main_layout.addWidget(video_label)
        main_layout.addWidget(location_label)
        main_layout.addWidget(self.speech_text)
        main_layout.addWidget(self.keyboard_input)

        self.setLayout(main_layout)

    def start_speech_recognition(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak now...")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            self.speech_text.setText(f"Speech-to-Text Output: {text}")
            self.process_command(text)
        except sr.UnknownValueError:
            self.speech_text.setText("Speech-to-Text Output: Could not understand audio")
        except sr.RequestError as e:
            self.speech_text.setText(f"Speech-to-Text Output: Error; {e}")

    def process_command(self, command):
        # Handle keyboard input and MQTT communication here
        self.keyboard_input.setText(f"Keyboard Input: {command}")
        mqtt_client.publish("car/commands", command)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.start_speech_recognition()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())