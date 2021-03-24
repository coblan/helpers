import pika
class AutoConnectBlockingPika(object):
    "会自动重连，自动判断channel"
    def __init__(self, host,port=5672,user='',password='', **kwargs):
        self.host = host
        self.port=port
        self.user=user
        self.password = password
        self.connection = None
        self.channel = None
    
    def getChannel(self):
        if not self.connection or self.connection.is_closed:
            credentials = pika.PlainCredentials(self.user,self.password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,port=self.port,credentials=credentials))
            self.channel = self.connection.channel()
        elif self.channel.is_closed:
            self.channel = self.connection.channel()
        return self.channel