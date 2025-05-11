import json

from asgiref.sync               import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers            import get_channel_layer
from chat.models                import Chat, Message
from prfl.models                import Profile, BlockedFriend
from django.core.exceptions     import ObjectDoesNotExist
from django.contrib.auth.models import User
from authentication.utils       import print_red, print_green, print_yellow
from asyncio                    import Lock

user_connections = {}
connections_lock = Lock()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        print_red(f'USER ... websocket: {self.user.username}')
        if not self.user or not self.user.is_authenticated:
            await self.close()
        
        await self.accept()
        print_green('websocket .... connections accpted')
        async with connections_lock:
            user_connections[self.user.username] = self.channel_name

    async def disconnect(self, code):
        async with connections_lock:
            if self.user.username in user_connections:
                del user_connections[self.user.username]
        print_red('websocket ... connection closed')

    async def receive(self, text_data):
        print_green('websocket ... receiving')
        data_json = json.loads(text_data)

        if not data_json:
            await self.error({
                'type': 'error',
                'error': 'no data received.'
            })
            return

        action = data_json.get('action')
        target_username = data_json.get('username')
        if not action or not target_username:
            await self.error({
                'type': 'error',
                'error': 'action and target user.'
            })
            return

        username = await sync_to_async(self.get_username)()
        profile = await sync_to_async(self.get_profile)(self.user)
        try:
            user = await sync_to_async(Profile.objects.get)(username=target_username)
        except Profile.DoesNotExist:
            pass

        is_blocked = await sync_to_async(
                lambda: BlockedFriend.objects.filter(
                    blocker__in=[profile, user], blocked_friend__in=[profile, user]
                ).exists()
            )()
        if is_blocked:
            await self.error({
                'type': 'error',
                'error': 'You are blocked from chatting with this user.'
            })
            return

        user_id = await sync_to_async(self.get_id)(profile)
        target_id = await sync_to_async(self.get_id)(user)
        room_name = f"{user_id}-{target_id}" if user_id >= target_id else f"{target_id}-{user_id}"

        print_yellow(room_name)
        if action == 'create_room':
            await self.create_room(data_json, profile, user, room_name)
        elif action == 'chat_message':
            await self.send_message(data_json, username, target_username, profile, user, room_name)
        elif action == 'read_receipt':
            await self.set_read(data_json, username, target_username, room_name)

    async def create_room(self, data_json, profile, user, room_name):
        try:
            chat = await sync_to_async(Chat.objects.get)(name=room_name)
        except Chat.DoesNotExist:
            chat = await sync_to_async(Chat.objects.create)(
                user1=profile,
                user2=user,
                name=room_name
            )

    async def send_message(self, data_json, username, target_username, profile, user, room_name):
        message_content = data_json.get('message')

        if not message_content:
            await self.error({
                'type': 'error',
                'error': 'no message is provided.'
            })
            return
        
        print_yellow(message_content)
        try:
            chat = await sync_to_async(Chat.objects.get)(name=room_name)
        except Chat.DoesNotExist:
            await self.error({
                'type': 'error',
                'error': 'No chat found.'
            })
            return
        
        message = await sync_to_async(Message.objects.create)(
            chat=chat,
            sender=profile,
            receiver=user,
            content=message_content
        )
        created_at =  await sync_to_async(self.get_time)(message)
        message_data = {
                'type': 'chat_message',
                'from': username,
                'to': target_username,
                'message': message_content,
                'created_at':created_at,
        }
        async with connections_lock:
            target_channel = user_connections.get(target_username)
            if target_channel:
                print_red("exist")
                await self.channel_layer.send(
                    target_channel,
                    message_data
                )

    async def set_read(self, data_json, username, target_username, room_name):
        print_green("Messages READ")
        try:
            chat = await sync_to_async(Chat.objects.get)(name=room_name)
        except Chat.DoesNotExist:
            await self.error({
                'type': 'error',
                'error': 'No chat found.'
            })
            return
        
        messages = await sync_to_async(list)(chat.messages.all())
        await sync_to_async(self.update)(messages)
        message_data = {
                'type': 'read_receipt',
                'from': username,
                'to': target_username
        }
        async with connections_lock:
            target_channel = user_connections.get(target_username)
            if target_channel:
                print_red("exist")
                await self.channel_layer.send(
                    target_channel,
                    message_data
                )
            
    async def chat_message(self, event):
        print_green('websocket ... send message to websocket')
        print(event)
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'from': event['from'],
            'to': event['to'],
            'message': event['message'],
            'created_at': event['created_at']
        }))

    async def read_receipt(self, event):
        print_green('websocket ... send read to websocket')
        print(event)
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'from': event['from'],
            'to': event['to']
        }))

    async def error(self, event):
        print_green('websocket ... send error to websocket')
        print(event)
        await self.send(text_data=json.dumps({
            'type': 'error',
            'error': event['error']
        }))
        
    def get_profile(self, user):
        return user.profile
    def get_username(self):
        return self.user.username
    def get_time(self, message):
        return message.created_at.isoformat()
    def get_id(self, profile):
        return profile.id
    def update(self, messages):
        for message in messages:
            if not message.is_read:
                message.is_read = True
                message.save(update_fields=['is_read'])
