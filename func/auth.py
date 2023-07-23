from django.contrib.auth.models import User,Group
from helpers.func.random_str import get_str,unique_random,get_random_number,get_date_sequence,get_short_date_sequence,short_uuid

def make_user(prefix=None,password=None):
     if prefix:
          number = short_uuid(u=4)
          username =f'{prefix}{number}'
     else:
          username = short_uuid(u=4)
          
     while User.objects.filter(username=username).exist():
          if prefix:
               number = short_uuid(u=4)
               username =f'{prefix}{number}'
          else:
               username = short_uuid(u=4)
               
     user = User.objects.create(username)
     if password:
          user.set_password(password)
     else:
          password = get_str()
          user.set_password(password)
     return user,password
