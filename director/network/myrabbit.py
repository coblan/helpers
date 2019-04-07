from django.conf import settings
import pika

#rabbitChanel=None

def get_rabbit_chanel():
    global rabbitChanel
    credentials = pika.PlainCredentials(settings.RABBIT_USER,settings.RABBIT_PSWD)
    connection =pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_SERVER,credentials=credentials))
    rabbitChanel = connection.channel()
    return rabbitChanel

#rabbit_init()