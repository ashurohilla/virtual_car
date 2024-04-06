# mqtt_client.py

import random
import time
import threading
from paho.mqtt import client as mqtt_client
import keyboard

broker = 'broker.emqx.io'
port = 1883
gyroscope_topic = "gyroscope/data"

client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'test'
password = 'test'

# Define a global variable to store gyroscope data
gyroscope_data = None

def connect_mqtt(on_message_callback):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(gyroscope_topic)
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message_callback
    client.connect(broker, port)
    return client

def on_message(client, userdata, msg):
    global gyroscope_data
    if msg.topic == gyroscope_topic:
        gyroscope_data = msg.payload.decode()

def start_gyro_client():
    client = connect_mqtt(on_message)
    client.loop_start()

    while True:
        time.sleep(1)
