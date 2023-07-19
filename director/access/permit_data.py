# encoding:utf-8
import sqlite3
import json
import threading
from ..model_func.dictfy import model_to_name
db = sqlite3.connect(':memory:', check_same_thread=False)

cur = db.cursor()
cur.execute(''' CREATE TABLE permit (
name TEXT UNIQUE,
content TEXT,
info TEXT,
type TEXT
)''')

"""
type:model,set,single
"""

lock = threading.Lock()

def add_permits(permits): 
    try:
        lock.acquire(True)
        cur.executemany('''INSERT INTO permit VALUES (?,?,?,?)''', permits)
        db.commit()
    finally:
        lock.release()

def get_model_permit(names, model):
    try:
        lock.acquire(True)
        for per in cur.execute("""SELECT content FROM permit WHERE name IN (%s) AND type='set' """ % ','.join(["'%s'" % name for name in names]) ):
            names .extend(per[0].split(';'))
            
        for per in cur.execute("""SELECT content,name FROM permit WHERE name IN (%s) AND info='%s' AND type='model' """ % ( ','.join(["'%s'" % name for name in names]), model_to_name(model)) ):
            content_dc = json.loads( per[0] )
            content_dc['name']=per[1]
            yield content_dc
    finally:
        lock.release()

def expand_permit_names(names): 
    inn_names = list(names)
    try:
        lock.acquire(True)
        for per in cur.execute("""SELECT content FROM permit WHERE name IN (%s) AND type='set' """ % ','.join(["'%s'" % name for name in names]) ):
            inn_names .extend(per[0].split(';'))
    finally:
        lock.release()
    return inn_names  


def model_read_permit(model,write=[],exclude=[]): 
    fields = model._meta.get_fields()
    permit = {
        'read': [f.name for f in fields if f.name not in exclude],
        'write': write,
        '_can_create': False,
        '_can_delete': False,
    }
    return json.dumps( permit )    

def model_full_permit(model,exclude=[],write_exclude=[],create=True,delete=True): 
    fields = model._meta.get_fields()
    fields=[x for x in fields if x.name not in exclude]  
    permit = {
        'read': [f.name for f in fields],
        'write': [f.name for f in fields if f.name not in write_exclude],
        '_can_create': create,
        '_can_delete': delete,
    }
    return json.dumps( permit )