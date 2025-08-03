# chatBoot/middleware.py
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
import sys
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            query_string = parse_qs(scope["query_string"].decode())
            token = query_string.get("token", [None])[0]

            if token:
                user = await self.get_user(token)
                scope["user"] = user
            else:
                scope["user"] = AnonymousUser()
        except Exception as e:
            print("JWT Middleware Error:", e)
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        token = AccessToken(token)
        user_id = token.payload['user_id']
        user = User.objects.get(id=user_id)
        return user