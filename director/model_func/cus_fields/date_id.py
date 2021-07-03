from django.db import models
from helpers.director.kv import get_value
from django.utils import timezone

class DateIdField(models.IntegerField):

    def __init__(self,length=5,key='_dateid', *args, **kwargs):
        self.date = timezone.now().strftime('%Y%m%d')
        self.char_len = char_len
        super().__init__(*args, **kwargs)


    def pre_save(self, model_instance, add):
        """
        Returns field's value just before saving.
        """
        if getattr(model_instance,self.name,'') =='':
            while True:
                char_id = get_str(length=self.char_len)
                dc = {self.name:char_id}
                if not  model_instance._meta.model.objects.filter(**dc).exists():
                    setattr(model_instance,self.name,char_id )
                    break
        return super().pre_save(model_instance, self.attname)    