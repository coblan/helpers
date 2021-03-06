from .models import KVModel
import json

def get_json(key,default=None,gte=None):
    value = get_value(key,gte=gte)
    if value is not None and value !='':
        return json.loads(value)
    else:
        return default

def set_json(key,value):
    myvalue = json.dumps(value,ensure_ascii=False)
    set_value(key,myvalue)

def get_value(key,default=None,gte=None):
    try:
        if gte:
            inst=KVModel.objects.get(key=key,update__gte=gte)
        else:
            inst=KVModel.objects.get(key=key)
        return inst.value
    except KVModel.DoesNotExist:
        return default

def set_value(key,value):
    KVModel.objects.update_or_create(key=key,defaults={'value':value})
    
def clear_value(key):
    KVModel.objects.filter(key=key).delete()

def update_value(key,oldvalue,newvalue):
    return KVModel.objects.filter(key=key,value=oldvalue).update(value=newvalue)

def lock_created(key,value):
    obj,created = KVModel.objects.update_or_create(key=key,defaults={'value':value})
    return created