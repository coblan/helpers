import random

def get_str(length=15):
    a='abcdefghijklmnopqrstuvwxyz'
    a+=a.upper()
    a += '1234567890'
    return ''.join([random.choice(a) for i in range(length)])