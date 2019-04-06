# encoding:utf-8
import sqlite3
import json
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
def add_permits(permits): 
    cur.executemany('''INSERT INTO permit VALUES (?,?,?,?)''', permits)
    db.commit()


def get_model_permit(names, model):
    
    for per in cur.execute("""SELECT content FROM permit WHERE name IN (%s) AND type='set' """ % ','.join(["'%s'" % name for name in names]) ):
        names .extend(per[0].split(';'))
        
    for per in cur.execute("""SELECT content FROM permit WHERE name IN (%s) AND info='%s' AND type='model' """ % ( ','.join(["'%s'" % name for name in names]), model_to_name(model)) ):
        yield json.loads( per[0] )

def expand_permit_names(names): 
    inn_names = list(names)
    for per in cur.execute("""SELECT content FROM permit WHERE name IN (%s) AND type='set' """ % ','.join(["'%s'" % name for name in names]) ):
        inn_names .extend(per[0].split(';'))
    return inn_names  


def model_read_permit(model): 
    fields = model._meta.get_fields()
    permit = {
        'read': [f.name for f in fields],
        'write': [],
        '_can_create': False,
        '_can_delete': False,
    }
    return json.dumps( permit )    

def model_full_permit(model): 
    fields = model._meta.get_fields()
    permit = {
        'read': [f.name for f in fields],
        'write': [f.name for f in fields],
        '_can_create': True,
        '_can_delete': True,
    }
    return json.dumps( permit )