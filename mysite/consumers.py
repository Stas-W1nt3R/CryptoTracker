import json
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer


class CryptoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_layer = get_channel_layer()
        await self.channel_layer.group_add('cryptocurrency', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('cryptocurrency', self.channel_name)

    async def send_price(self, event):
        await self.send(text_data=json.dumps(event))