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
            self.stored_messages = ''
            await self.accept()

    async def disconnect(self, close_code):
        print(f"🔴 {self.scope['user'].username} DISCONNECTED", file=sys.stderr)

    async def receive(self, text_data):
        print("📥 RECEIVED data", file=sys.stderr)
        print(self.stored_messages, file=sys.stderr)
        text_data_json = json.loads(text_data)
        event = text_data_json["event"]
        if event == 'newMessage':
            await self.treatingMessage(text_data_json)
        if event == "newRoom":
            await self.createRoom()
        if event == 'reconnect':
            await self.rejoin_room(text_data_json)
            pass
       
    async def treatingMessage(self, text_data_json):
        message = text_data_json["message"]
        prompt = await self.get_chat_hestory()
        prompt.append({'role': 'user', 'parts': [message]})
        respons =  self.get_gemini_response(prompt)
        await self.send(text_data=json.dumps({"message": respons}))
        await self.storeMessages(message, respons)
        await self.get_chat_hestory()

    @database_sync_to_async
    def storeMessages(self, message, response):
        Message.objects.create(user=self.user, room=self.room, sender='user', message=message)
        Message.objects.create(user=self.user, room=self.room, sender='model', message=response)

    @database_sync_to_async
    def createRoom(self):
        user = self.scope['user'] 
        self.room = Room.objects.create(title='movie', user=user)

    @database_sync_to_async
    def get_chat_hestory(self):
        print("get", file=sys.stderr)
        messages = Message.objects.filter(room=self.room).order_by('date').values()
        history = [{"role": "user",  # This is the instruction, even though it's role=user
        "parts": [
            "You are CineBrain, a helpful assistant that ONLY answers questions related to movies, actors, directors, genres, ratings, or cinematic analysis. "
            "ask anything relaited to movies like(a country movies, actor movies, type of movies)"
            "If the user asks anything outside this scope (like math, weather, politics, personal help)', politely decline by saying: "
            "'I can only help with movie-related questions.'"
            "'if user asks anything related to name israel, politely decline by saying:'"
            "'Sorry can't say anything related to keyword (israel)'"
        ]}]
        stored_messages = []
        for idx, message in enumerate(messages):
            part = message.get('message')
            sender = message.get('sender')
            stored_messages.append({'sender': sender, 'message': [part]})
            history.append({'role': sender, 'parts': [part]})
        self.stored_messages = stored_messages
        return history
    
    @database_sync_to_async
    def rejoin_room(self, text_data_json):
        room = int(text_data_json['room_id'], base=10)
        self.room = Room.objects.get(id=room)
        pass
