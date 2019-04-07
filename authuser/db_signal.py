from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from .models import UserInfo
from .base_data import authuser_dc

"""
这里的事件handler 只保证每个usr 都有对应的profile
必须要保证 model有以下字段
user=models.OneToOneField(User,verbose_name='账号',null=True)
"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and authuser_dc.get('TUserinfo') :
        TUserinfo=authuser_dc.get('TUserinfo')
        TUserinfo.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
    #instance.profile.save()