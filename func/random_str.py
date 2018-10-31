import random

def get_str(length=15):
    a='abcdefghijklmnopqrstuvwxyz'
    a+=a.upper()
    a += '123456789012345678901234567890123456789012345678901234567890'  # 为了数字和字母出现的概率相近
    return ''.join([random.choice(a) for i in range(length)])

def get_random_number(length= 6): 
    a = '1234567890'  
    return ''.join([random.choice(a) for i in range(length)])