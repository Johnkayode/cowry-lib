
import json
import pika
from decouple import AutoConfig
from api.utils import process_message


config = AutoConfig()

class RabbitMQClient:
    _instance = None

    def __init__(self, url):
        self.url = url
        self.connection = None
        self.channel = None
       
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def connect(self):
        if not self.connection:
            params = pika.URLParameters(self.url)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()

    def publish(self, queue_name: str, message_content: json):
        self.connect()
        self.channel.queue_declare(queue_name)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message_content),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )

    def on_message(self, ch, method, properties, body) -> None:
        message = json.loads(body)
        data = message.pop("data")
        process_message(event=message["event_type"], data=data)

    def consume(self, queue_name: str):
        self.connect()
        # Declare the queue
        self.channel.queue_declare(queue=queue_name)
        # Start consuming messages from the queue
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.on_message)
        print(f" [*] Waiting for messages in queue {queue_name}. To exit press CTRL+C")
        self.channel.start_consuming()

    def close(self):
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()


rabbitmq_client = RabbitMQClient(url=config("AMQP_URL", default="amqp://guest:guest@rabbitmq:5672/"))