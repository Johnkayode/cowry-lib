from django.core.management.base import BaseCommand
from rabbitmq import rabbitmq_client  


class Command(BaseCommand):
    help = 'Run the RabbitMQ consumer'

    def handle(self, *args, **kwargs):
        try:
            rabbitmq_client.consume('core_updates')
        except KeyboardInterrupt:
            print("[x] Consumer stopped manually.")
        finally:
            rabbitmq_client.close()