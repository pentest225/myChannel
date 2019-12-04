# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
import json
from . import models

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print("################# Romm name ########################")
        print(self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name
        # insertion du salon en base de bonne 
        
            #1 verifion si le salon n'existe pas en bd 
        if models.Salon.objects.filter(nom=self.room_name).exists():
            print("ok existe ")
        else:
            new_salon = models.Salon(nom=self.room_name,user=self.scope['user'])
            new_salon.save()
            print("new salon is saving ")
        # print (obj.nom)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data)
        message = text_data_json['message']
        user_name = text_data_json['user']

        curent_user=User.objects.get(username=user_name)
        curent_romm=models.Salon.objects.get(nom=self.room_name)
        # Enregistrement du message en bd 
        newMessage = models.Message(salon=curent_romm,user=curent_user,message=message)
        newMessage.save()
        print(newMessage)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))