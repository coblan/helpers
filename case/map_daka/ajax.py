from .models import DakaRecord
import json
def get_global():
    return globals()

def daka(pos,user):
    pos=json.dumps(pos)
    DakaRecord.objects.create(user=user,pos=pos)
    return {'status':'success'}

