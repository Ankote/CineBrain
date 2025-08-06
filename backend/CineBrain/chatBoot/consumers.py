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
            self.hisstory_messages = []
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
        if event == 'reconnect':
           
            room_id = text_data_json.get('room_id')

            if room_id is None:
                await self.send(text_data=json.dumps({
                    "error": "Missing 'room_id' in message"
                }))
                return

            try:
                self.room =  await self.rejoin_room(text_data_json)
            except Room.DoesNotExist:
                await self.send(text_data=json.dumps({
                    "error": "Room not found."
                }))


    async def treatingMessage(self, text_data_json):
        message = text_data_json["message"]
        if len(self.hisstory_messages) == 0:
            self.hisstory_messages = await self.get_chat_hestory()
        self.hisstory_messages.append({'role': 'user', 'parts': [message]})
        respons =  self.get_gemini_response(self.hisstory_messages)
        # messages = self.reformatingMessages()
        # print((messages), file=sys.stderr)
        await self.send(text_data=json.dumps({
            "action": 'listingMessages',
            'messages' : self.hisstory_messages[1:]
        }))

        await self.storeMessages(message, respons)

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
        for idx, message in enumerate(messages):
            part = message.get('message')
            sender = message.get('sender')
            history.append({'role': sender, 'parts': [part]})
        return history
    
    @database_sync_to_async
    def rejoin_room(self, text_data_json):
        room = int(text_data_json.get('room_id'), base=10)
        self.room = Room.objects.get(id=room)

    def reformatingMessages(self):
        messages = {}
        for message in self.hisstory_messages[1:]:
            sender = message.get('role')
            msg = message.get('parts')
            messages[sender] = msg
        print(messages, file=sys.stderr)
        return messages
