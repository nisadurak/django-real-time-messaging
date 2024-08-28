from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Modelleri burada içe aktarın
        from django.contrib.auth.models import User
        from .models import Message

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        from django.contrib.auth.models import User
        from .models import Message

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def chat_message(self, event):
        from django.contrib.auth.models import User
        from .models import Message

        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    async def receive(self, text_data):
        from django.contrib.auth.models import User
        from .models import Message

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope["user"].username

        user = await sync_to_async(User.objects.get)(username=username)

        await sync_to_async(Message.objects.create)(user=user, room=self.room_name, content=message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )
