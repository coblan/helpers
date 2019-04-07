from django.conf import settings
import pika

def get_rabbit_instance():
    credentials = pika.PlainCredentials(settings.RABBIT_USER,settings.RABBIT_PSWD)
    connection =pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_SERVER,credentials=credentials))
    channel = connection.channel()
    return channel