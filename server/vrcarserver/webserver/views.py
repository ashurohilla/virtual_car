# views.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CarControlConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'car_control'
        self.room_group_name = f'car_control_{self.room_name}'

        # Join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'car_control_message',
                'message': message
            }
        )

    # Receive message from the group
    async def car_control_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))