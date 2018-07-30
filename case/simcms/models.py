from django.db import models

# Create your models here.
class CmsPageModel(models.Model):
    name = models.CharField('url名', max_length = 60, unique = True)
    label = models.CharField('名称', max_length = 200)
    temp_cls = models.CharField('模板', max_length = 200)
    enable = models.BooleanField('启用', default = True)
    detail = models.TextField('描述', blank = True)
    par = models.ForeignKey('CmsPageModel', verbose_name = '继承', blank = True, null = True)
    content = models.TextField('内容', blank= True)
    update_time = models.DateTimeField('更新时间', auto_now= True, editable = True)
    
    def __unicode__(self): 
        return self.label