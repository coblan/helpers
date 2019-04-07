import random


from uuid import uuid4
uuidChars = ("a", "b", "c", "d", "e", "f",
       "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
       "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
       "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
       "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
       "W", "X", "Y", "Z")
def short_uuid():
  uuid = str(uuid4()).replace('-', '')
  result = ''
  for i in range(0,8):
    sub = uuid[i * 4: i * 4 + 4]
    x = int(sub,16)
    result += uuidChars[x % 0x3E]
  return result




def get_str(length=15):
    a='abcdefghijklmnopqrstuvwxyz'
    a+=a.upper()
    a += '123456789012345678901234567890123456789012345678901234567890'  # 为了数字和字母出现的概率相近
    return ''.join([random.choice(a) for i in range(length)])

def get_random_number(length= 6): 
    a = '1234567890'  
    return ''.join([random.choice(a) for i in range(length)])