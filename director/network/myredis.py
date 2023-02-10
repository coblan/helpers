import redis
from django.conf import settings
from helpers.func.dot_dict import read_dict_path
redis_conn = None

def redis_init():
    global redis_conn
    if not isinstance(redis_conn, redis.client.StrictRedis):
        redis_conn =redis.Redis(
            host=read_dict_path(settings,'REDIS.host'), port=read_dict_path(settings,'REDIS.port'), decode_responses=True,
            db=read_dict_path(settings,'REDIS.db'),password=read_dict_path(settings,'REDIS.password')) 
    #if not isinstance(redis_conn, redis.client.StrictRedis):
        #redis_conn = redis.StrictRedis(settings.REDIS_HOST,
                                       #settings.REDIS_PORT,
                                       #settings.REDIS_DB)    
    return redis_conn

redis_init()