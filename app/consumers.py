import json
from channels.generic.websocket import AsyncWebsocketConsumer
class MeetingConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.peerID = self.scope['url_route']['kwargs']['peerID']
		# Join room
		self.room_group_name = f"meeting"
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()
	
	async def disconnect(self, close_code):
		# Leave room
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type' : 'chat_message',
				'function' : 'userLeft',
				'parameter' : self.peerID
			}
		)
	
	# Receive message from web socket
	async def receive(self, text_data):
		data = json.loads(text_data)
		data['type'] ='chat_message'
		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name,
			data
		)

	# Receive message from room group
	async def chat_message(self, event):
		# Send message to WebSocket
		await self.send(text_data=json.dumps(event))