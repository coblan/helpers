from django.db import models
from helpers.director.kv import get_value
from django.utils import timezone
from helpers.func.snowflake import IdWorker

class SnowFlakeField(models.BigIntegerField):

    def __init__(self,sequence=0, *args, **kwargs):
        self.sequence=sequence
        if not 'editable' in kwargs:
            kwargs['editable'] =False
        super().__init__(*args, **kwargs)


    def pre_save(self, model_instance, add):
        """
        Returns field's value just before saving.
        """
        if not getattr(model_instance,self.name,None) :
            datacenter_id=0
            worker_id=0
            worker = IdWorker(datacenter_id,worker_id,self.sequence)
            idd = worker.get_id()
            setattr(model_instance,self.name,idd )
            #while True:
                #char_id = get_str(length=self.char_len)
                #dc = {self.name:char_id}
                #if not  model_instance._meta.model.objects.filter(**dc).exists():
                    #setattr(model_instance,self.name,char_id )
                    #break
        return super().pre_save(model_instance, self.attname)    