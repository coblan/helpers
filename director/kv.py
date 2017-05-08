from .models import KVModel

def get_value(key,default=None):
    try:
        inst=KVModel.objects.get(key=key)
        return inst.value
    except KVModel.DoesNotExist:
        return default