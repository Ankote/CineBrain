from channels.generic.websocket import AsyncWebsocketConsumer
import json
import sys
from django.contrib.auth.models import AnonymousUser
class ChatConsumer(AsyncWebsocketConsumer):
  
    async def connect(self):
        
        if isinstance(self.scope['user'], AnonymousUser):
            await self.close()
        else:
            print(f"🟢 {self.scope['user'].username} Connected", file=sys.stderr)
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"
            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        print(f"🔴 {self.scope['user'].username} DISCONNECTED", file=sys.stderr)
        # await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        print("📥 RECEIVED data", file=sys.stderr)
        print(self.scope["user"], file=sys.stderr)
        
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]

        print(message, file=sys.stderr)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "from":sender, "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["from"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"from":sender, "message": message}))
