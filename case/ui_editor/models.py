from django.db import models

# Create your models here.

class Page(models.Model):
    name = models.CharField('名称',max_length=50,primary_key=True)
    desp = models.TextField('说明',blank=True)
    content = models.TextField('内容',blank=True)
    
    def __str__(self):
        return self.name
    
    
