import random
from django.utils import timezone
from helpers.director.kv import get_value,set_value,update_value,lock_created,lock_kv_inst
from django.db import transaction
from uuid import uuid4,uuid1
uuidChars = ("a", "b", "c", "d", "e", "f",
       "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
       "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
       "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
       "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
       "W", "X", "Y", "Z")
def short_uuid(u=4):
  if u== 4:
    uuid_cal = uuid4
  elif u ==1:
    uuid_cal = uuid1
  uuid = str(uuid_cal()).replace('-', '')
  result = ''
  for i in range(0,8):
    sub = uuid[i * 4: i * 4 + 4]
    x = int(sub,16)
    result += uuidChars[x % 0x3E]
  return result

def unique_random(get_fun,check_fun,maxcount=5,count=0):
  if count > maxcount:
    raise UserWarning('search unique str extend %s'%maxcount)
  count +=1
  value = get_fun()
  if not check_fun(value):
    return unique_random(get_fun, check_fun,maxcount, count)
  else:
    return value

def get_str(length=15):
    a='abcdefghijklmnopqrstuvwxyz'
    a+=a.upper()
    a += '123456789012345678901234567890123456789012345678901234567890'  # 为了数字和字母出现的概率相近
    return ''.join([random.choice(a) for i in range(length)])

def get_random_number(length= 6): 
    a = '123456789' 
    a1 = '1234567890'
    rt = random.choice(a) + ''.join([random.choice(a1) for i in range(length-1)])
    return rt
  
@transaction.atomic
def get_date_sequence(key='_data_sequence',fill=6,how_many=1,remove_year_digit=0,time_group='date'):
  """以日期为依据，生成随机序列
  
  @key:在kv数据库里面的key，可以用默认的
  @remove_year_digit:有时候fill的位数太多了，可能会造成int类型溢出，所以增加可以移除 年份前面的前面两位，2022的  20基本是无用的。
  
  """
  now = timezone.now()
  if time_group=='date':
    date_str = now.strftime('%Y%m%d')[remove_year_digit:]
  elif time_group =='month':
    date_str = now.strftime('%Y%m')[remove_year_digit:]
  elif time_group =='year':
    date_str = now.strftime('%Y')[remove_year_digit:]
  
  inst  = lock_kv_inst(key,default='')
  v = inst.value
  #v = get_value(key,None)

  if v and v.startswith(date_str):
    date_str_length =len(date_str)
    #start = int(v[date_str_length-remove_year_digit:])+1
    start = int(v[date_str_length:])+1
  else:
    start = 1
  #time_str = now.strftime('%Y%m%d')
  #date_int = int( time_str[remove_year_digit :] ) * 10**fill

  #date_int = int( date_str[remove_year_digit :] ) * 10**fill  
  date_int = int( date_str ) * 10**fill 
  ls = [date_int+x for x in range(start,start+how_many) ]
  set_value(key,ls[-1])
  return ls

def get_short_date_sequence(how_many=1,start_date='2021-05-18',fill=5,key='_short_date_sequence'):
  now = timezone.now()
  day_span = ( now - timezone.datetime.strptime(start_date, '%Y-%m-%d') ).days
  now_int = day_span * 10**fill
  v= get_value(key,None)
  if v is None or int(v) < now_int:
    start = now_int
  else:
    start = int( get_value(key,0) ) +1
    
  ls = list(  range(start,start+how_many) )
  if v is None:
    if not lock_created(key,ls[-1]):
      return get_short_date_sequence(how_many,start_date,fill,key)
  else:
    count = update_value(key,v,ls[-1]) 
    if count == 0:
      return get_short_date_sequence(how_many,start_date,fill,key)
  return ls  


