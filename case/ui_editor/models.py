from django.db import models

# Create your models here.

PAGE_KIND=(
    (1,'普通组件'),
    (2,'slot组件')
)

class Page(models.Model):
    name = models.CharField('名称',max_length=50,primary_key=True)
    desp = models.TextField('说明',blank=True)
    sort = models.IntegerField('排序',default=0)
    content = models.TextField('内容',blank=True,default='[]')
    kind = models.IntegerField('类型',default=1,choices=PAGE_KIND)
    
    def __str__(self):
        return self.name
    
    
