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

def model_read_permit(model): 
    fields = model._meta.get_fields()
    permit = {
        'read': [f.name for f in fields],
        'write': [],
        'create': False,
        'delete': False,
    }
    return json.dumps( permit )    

def model_full_permit(model): 
    fields = model._meta.get_fields()
    permit = {
        'read': [f.name for f in fields],
        'write': [f.name for f in fields],
        'create': True,
        'delete': True,
    }
    return json.dumps( permit )