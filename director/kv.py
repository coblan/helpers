from .models import KVModel
import json

def get_json(key,default=None):
    value = get_value(key)
    if value is not None and value !='':
        return json.loads(value)
    else:
        return default

def set_json(key,value):
    myvalue = json.dumps(value,ensure_ascii=False)
    set_value(key,myvalue)

def get_value(key,default=None):
    try:
        inst=KVModel.objects.get(key=key)
        return inst.value
    except KVModel.DoesNotExist:
        return default

def set_value(key,value):
    KVModel.objects.update_or_create(key=key,defaults={'value':value})
    
def clear_value(key):
    KVModel.objects.filter(key=key).delete()

def lock_created(key,value):
    obj,created = KVModel.objects.update_or_create(key=key,defaults={'value':value})
    return created