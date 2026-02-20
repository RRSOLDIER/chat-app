import json
from datetime import datetime
from .models import Message
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

class OnlineStatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']

        if user.is_anonymous:
            await self.close()
            return

        self.group_name = "online_users"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        user.is_online = True
        await sync_to_async(user.save)()

        await self.accept()

        # ✅ BROADCAST ONLINE
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "user_status",
                "user_id": user.id,
                "status": "online"
            }
        )

    async def disconnect(self, close_code):
        user = self.scope['user']

        if user.is_anonymous:
            return

        user.is_online = False
        await sync_to_async(user.save)()

        # ✅ BROADCAST OFFLINE
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "user_status",
                "user_id": user.id,
                "status": "offline"
            }
        )

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def user_status(self, event):
        await self.send(text_data=json.dumps(event))


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)
        sender = self.scope["user"]

        if data.get("typing"):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_event",
                    "sender": sender.username
                }
            )
            return

        if data.get("delete_id"):
            delete_id = data.get("delete_id")

            await self.delete_message(delete_id)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "delete_event",
                    "delete_id": delete_id
                }
            )
            return

        message = data.get("message")
        receiver_id = data.get("receiver_id")

        if not message:
            return

        receiver = await self.get_receiver(receiver_id)

        if not receiver:
            return  # ✅ CRITICAL SAFETY

        msg_obj = await self.save_message(sender, receiver, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username,
                "message_id": msg_obj.id
            }
        )

    async def chat_message(self, event):

        await self.send(text_data=json.dumps(event))

    async def typing_event(self, event):

        await self.send(text_data=json.dumps({
            "typing": True,
            "sender": event["sender"]
        }))

    async def delete_event(self, event):

        await self.send(text_data=json.dumps({
            "delete_id": event["delete_id"]
        }))

    @sync_to_async
    def get_receiver(self, receiver_id):
        try:
            return User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return None

    @sync_to_async
    def save_message(self, sender, receiver, message):
        return Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=message
        )

    @sync_to_async
    def delete_message(self, msg_id):
        Message.objects.filter(id=msg_id).delete()
