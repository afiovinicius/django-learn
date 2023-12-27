import json


from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import InMemoryChannelLayer


class CursorConsumer(AsyncWebsocketConsumer):
    channel_layer: InMemoryChannelLayer

    async def connect(self):
        await self.channel_layer.group_add("cursors_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("cursors_group", self.channel_name)

    async def receive(self, text_data):
        cursor_data = json.loads(text_data)
        await self.channel_layer.group_send(
            "cursors_group",
            {
                'type': 'handle.cursor.move',
                'content': cursor_data,
            }
        )

    async def handle_cursor_move(self, event):
        cursor_data = event['content']

        await self.send(text_data=json.dumps(cursor_data))
