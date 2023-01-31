import uuid
import time
import redis
from helpers.director.network.myredis import redis_conn
import json

from contextlib import contextmanager

import logging
general_log = logging.getLogger('general_log')

def get_json(conn,key,default={}):
    json_str = conn.get(key)
    if json_str:
        return json.loads(json_str)
    else:
        return default

def set_json(conn,key,value):
    conn.set(key,json.dumps(value))

#@contextmanager
#def lock(conn,lockname,timeout=10):
    #lock_id = acquire_lock(conn, lockname, timeout)
    #if lock_id:
        #yield
        #release_lock(conn, lockname, lock_id)
    #else:
        #general_log.warning(f'获取redis{lockname}锁超时')
        ## 超时了，解锁一下，避免死锁了
        ##clear_lock(conn, lockname)

class lock(object):
    def __init__(self,conn,lockname,timeout=10):
        self.conn = conn
        self.lockname = lockname
        self.timeout = timeout
    
    def __enter__(self):
        self.lockid = acquire_lock(self.conn, self.lockname, self.timeout)
        if self.lockid:
            return self
        else:
            general_log.warning(f'获取redis{self.lockname}锁超时')
            raise UserWarning(f'获取redis{self.lockname}锁超时')
    
    def __exit__(self,exc_t, exc_v, traceback):
        release_lock(self.conn, self.lockname, self.lockid)
        return False

# 加锁的过程
def acquire_lock(conn, lockname, timeout = 10,ex=30):
    identifier = str(uuid.uuid4())
    end = time.time() + timeout
    while time.time() < end:
        # 这里尝试取得锁 setnx 设置-如果不存在的时候才会set
        #conn.setnx('lock:' + lockname, identifier)
        conn.set('lock:' + lockname,identifier,nx=True,ex=ex)
        if conn.get('lock:' + lockname)==identifier:
            general_log.debug(f'获得redis锁:{lockname}.{identifier}')
            return identifier
        #if conn.setnx('lock:' + lockname, identifier): 
            ## 获得锁之后输出获得锁的‘进程’号
            ##print('获得锁:进程'+ str(args))
            #general_log.debug(f'获得redis锁:{lockname}.{identifier}')
            #return identifier
    return False


def release_lock(conn, lockname, identifier):
    "释放锁"
    pipe = conn.pipeline(True)
    lockname = 'lock:' + lockname
    while True:
        try:
            pipe.watch(lockname)
            #identifier_real = pipe.get(lockname).decode()
            identifier_real = pipe.get(lockname)
            if identifier_real == identifier:
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                general_log.debug(f'释放redis锁:{lockname}.{identifier}')
                return True
            pipe.unwatch()
            break
        except redis.exceptions.WatchError:
            pass
    return False

def clear_lock(conn,lockname):
    lockname = 'lock:' + lockname
    conn.delete(lockname)
    general_log.debug(f'清除redis锁:{lockname}')