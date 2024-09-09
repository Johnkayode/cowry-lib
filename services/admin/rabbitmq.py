import asyncio
import json

from aio_pika import connect, Connection, Channel, Message, IncomingMessage
from api.utils import process_message

class RabbitMQClient:
    _instance = None

    def __init__(self, url):
        self.url = url
        self.connection: Connection = None
        self.channel: Channel = None
        self.consume_task: asyncio.Task = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def connect(self):
        if not self.connection:
            self.connection = await connect(self.url)
            self.channel = await self.connection.channel()

    async def publish(self, queue_name: str, message_content: json):
        await self.connect()
        queue = await self.channel.declare_queue(queue_name)
        await self.channel.default_exchange.publish(
            Message(json.dumps(message_content).encode()),
            routing_key=queue.name,
        )

    async def on_message(self, message: IncomingMessage) -> None:
        async with message.process():
            message_ = json.loads(message.body.decode())
            data = message_.pop("data")
            process_message(event=message_["event_type"], data=data)

    async def consume(self, queue_name: str):
        await self.connect()
        channel = await self.connection.channel()
        queue = await channel.declare_queue(queue_name)
        await queue.consume(self.on_message, no_ack=False)        

    async def start_consume(self, queue_name: str):
        self.consume_task = asyncio.create_task(self.consume(queue_name))
       

    async def close(self):
        if self.consume_task:
            self.consume_task.cancel()
            try:
                await self.consume_task
            except asyncio.CancelledError:
                pass
            except Exception as unexpected_exception:
                print("Unexpected exception has occurred")

        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()