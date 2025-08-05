import json
import logging
from channels.generic.websocket import WebsocketConsumer
from asgiref import async_to_sync

logger = logging.getLogger(__name__)

class CarControlConsumer(WebsocketConsumer):
    groups = ["broadcast"]

    def connect(self):
        self.roomname = "test_raspberry_pi "
        self.room_group_name = " test-raspberrypi_group"

        async_to_sync(self.channel_layer.group_add)(
            self.roomname, self.room_group_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status': 'connected django cchannels'}))
        logger.info("WebSocket connection established.")

    def disconnect(self, close_code):
        logger.info("WebSocket connection closed.")

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            command = text_data_json['command']
            self.send_command_to_raspberry_pi(command)
        except json.JSONDecodeError as e:
            logger.error("Error decoding JSON: %s", e)
        except KeyError as e:
            logger.error("Missing 'command' key in JSON: %s", e)
        except Exception as e:
            logger.error("An error occurred: %s", e)

    def send_command_to_raspberry_pi(self, command):
        try:
            # Implementation to send the command to the Raspberry Pi
            # over a WebSocket or other communication channel
            logger.info(f"Sending command to Raspberry Pi: {command}")
            # Code to send command to Raspberry Pi goes here
        except Exception as e:
            logger.error("Error sending command to Raspberry Pi: %s", e)
