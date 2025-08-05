from channels.generic.websocket import AsyncWebsocketConsumer
import json
import sys
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from .models import Room, Message
from .serializers  import MessageSerializer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
  
    async def connect(self):
        
        if isinstance(self.scope['user'], AnonymousUser):
            print("🔴 ACCESS DENIED!!", file=sys.stderr)
            await self.close()
        else:
            from .gemini_client import get_gemini_response
            self.get_gemini_response = get_gemini_response
            print(f"🟢 {self.scope['user'].username} Connected", file=sys.stderr)
            self.user = self.scope['user']
            self.room = ""
            await self.accept()

    async def disconnect(self, close_code):
        print(f"🔴 {self.scope['user'].username} DISCONNECTED", file=sys.stderr)

    async def receive(self, text_data):
        print("📥 RECEIVED data", file=sys.stderr)
        text_data_json = json.loads(text_data)
        event = text_data_json["event"]
        if event == 'newMessage':
            await self.treatingMessage(text_data_json)
        if event == "newRoom":
            await self.createRoom()
       
    async def treatingMessage(self, text_data_json):
        message = text_data_json["message"]
        prompt = message
        prompt = [
    {"role": "user", "parts": ["Hello"]},
    {"role": "model", "parts": ["Hi, how can I assist you today?"]},
    {"role": "user", "parts": ["What's the weather like in Paris?"]},
    {"role": "model", "parts": ["I can't give you a real-time, up-to-the-minute weather forecast.?"]},
    {"role": "user", "parts": ["can tell me what is the first question i asked you in this conversation"]},
]
        respons =  self.get_gemini_response(prompt)
        await self.send(text_data=json.dumps({"message": respons}))
        await self.storeMessages(message, respons)
        

    @database_sync_to_async
    def storeMessages(self, message, response):
        Message.objects.create(user=self.user, room=self.room, sender='H', message=message)
        Message.objects.create(user=self.user, room=self.room, sender='AI', message=response)

    @database_sync_to_async
    def createRoom(self):
        print("room", file=sys.stderr)
        user = self.scope['user'] 
        self.room = Room.objects.create(title='movie', user=user)

    @database_sync_to_async
    def get_chat_hestory(self):
        messages = Message.objects.filter(room=self.room).order_by('-date')
        
        