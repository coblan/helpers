from django.core.mail.backends.base import BaseEmailBackend
 
class MyEmailBackend(BaseEmailBackend):
    def send_messages(email_messages):
        print(email_messages)
    
 