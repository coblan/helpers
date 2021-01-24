from django.db import models
from helpers.func.random_str import get_str

class CharIdField(models.CharField):

    def __init__(self,char_len=6, *args, **kwargs):
        self.char_len = char_len
        super().__init__(*args, **kwargs)

    #def from_db_value(self,value, *args,**kws):
        #if not value:
            
        #return super().from_db_value(value,*args,**kws)

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