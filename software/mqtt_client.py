import random
import time
import threading
from paho.mqtt import client as mqtt_client
import keyboard

broker = 'broker.emqx.io'
port = 1883
left_right_topic = "python/left_right"
forward_backward_topic = "python/forward_backward"

client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'test'
password = 'test'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            # Subscribe to topics here if needed
            client.subscribe(left_right_topic)
            client.subscribe(forward_backward_topic)
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

def publish(client, topic, text):
    result = client.publish(topic, text)
    status = result[0]
    if status == 0:
        print(f"Sent `{text}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def take_input():
    command = "stop"  # Default command
    if keyboard.is_pressed('w'):
        command = "forward"
    elif keyboard.is_pressed("s"):
        command = "backward"
    if keyboard.is_pressed("a"):
        command += " left"
    elif keyboard.is_pressed("d"):
        command += " right"
    return command.strip()

def mqtt_publish_task(client):
    while True:
        command = take_input()
        commands = command.split()
        for cmd in commands:
            if cmd == "left" or cmd == "right":
                publish(client, left_right_topic, cmd)
            elif cmd == "forward" or cmd == "backward":
                publish(client, forward_backward_topic, cmd)
        time.sleep(0.2)

def start_mqtt_client():
    mqtt_client = connect_mqtt()
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    mqtt_publish_thread = threading.Thread(target=mqtt_publish_task, args=(mqtt_client,))
    mqtt_publish_thread.daemon = True
    mqtt_publish_thread.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    start_mqtt_client()
