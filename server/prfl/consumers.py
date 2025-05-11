import json
from channels.generic.websocket         import AsyncWebsocketConsumer
from channels.layers                    import get_channel_layer
from .utils.connections_manager         import connected_clients, clients_lock
from authentication.utils               import print_red, print_green, print_yellow
from asgiref.sync                       import sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope["user"]
        if self.user == None:
            await self.close()
        await self.accept()
        async with clients_lock:
            print_green('Notification websocket .... connections accpted')
            connected_clients[self.user.username] = self.channel_name
        profile = await sync_to_async(self.get_profile)(self.user)
        await sync_to_async(self.update_profile)(profile, True)
        print_yellow(self.user.username)
        for user, channel_name in connected_clients.items():
                print(f"User: {user}, Channel Name: {channel_name}")

    async def disconnect(self, close_code):
        print_red('Notification websocket ... connection closed')
        async with clients_lock:
            if self.user.username in connected_clients:
                del connected_clients[self.user.username]
        profile = await sync_to_async(self.get_profile)(self.user)
        await sync_to_async(self.update_profile)(profile, False)

    async def receive(self, text_data):
        pass

    async def send_friendship_request(self, event):
        await self.send(text_data=json.dumps({
            "type": "friendship_request",
            "from": event["from"]
        }))

    async def handle_friendship_request(self, event):
        await self.send(text_data=json.dumps({
            "type": "handle_friendship_request",
            "from": event["from"],
            "status": event["status"]
        }))

    async def send_playwithme_request(self, event):
        await self.send(text_data=json.dumps({
            "type": "send_playwithme_request",
            "from": event["from"]
        }))

    async def join_tournament_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "join_tournament_notification",
            "from": event["from"],
            "tournament_name": event["tournament_name"]
        }))
        
    async def tournament_reminder_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "tournament_reminder_notification"
        }))

    def update_profile(self, profile, flg):
        profile.is_online = flg
        profile.save(update_fields=['is_online'])
            
    def get_profile(self, user):
        return user.profile
    