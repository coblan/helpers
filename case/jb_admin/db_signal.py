from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
#from eface.wechat.models import WxInfo
from helpers.director.models import PermitModel 
from django.contrib.auth.models import Group,User

@receiver(post_save, sender=Group)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PermitModel.objects.create(group = instance)

 