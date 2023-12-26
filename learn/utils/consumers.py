import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CursorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        cursor_data = json.loads(text_data)

        await self.send(text_data=json.dumps({
            'type': 'cursor.move',
            'cursor_data': cursor_data,
        }))
