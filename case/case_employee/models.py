# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models
from django.utils.translation import ugettext as _
from helpers.director.model_validator import has_str


GEN=(
    ('male',_('male')),
    ('femal',_('femal'))
    )

class BasicInfo(models.Model):
    name = models.CharField(_('name'), max_length=50, blank=True)
    age = models.CharField(_('age'), max_length=50, blank=True)
    head = models.CharField(_('head image'),max_length=200,blank=True,default='/static/res/image/user.jpg')
    id_number=models.CharField(_('id  number'),max_length=200,blank=True)
    address=models.CharField(_('address'),max_length=500,blank=True)
    gen = models.CharField(_('gen'),max_length=30,blank=True,choices=GEN)
    phone = models.CharField(_('phone'),max_length=100,blank=True)


    def __unicode__(self):
        return self.name

class Department(models.Model):
    name=models.CharField(_('department name'),max_length=500,default='new department',validators=[has_str])
    par = models.ForeignKey('self',verbose_name=_('parent department'),blank=True,null=True,related_name='childs')
    detail=models.TextField(verbose_name=_('detail'),blank=True)
    par_chain=models.CharField('parent chain',max_length=200,blank=True)

    def __unicode__(self):
        return self.name
    
    def __init__(self,*args,**kw):
        super(Department,self).__init__(*args,**kw)
        self._org_par=self.par

    def save(self, *args,**kw):   
        rt= super(Department,self).save(*args,**kw)
        if self._org_par !=self.par or not self.par_chain:
            self._org_par=self.par
            self.update_parent_chain()  
        return rt
    
    def update_parent_chain(self):
        par =self.par
        ls=[self.pk]
        while par:
            ls.append(par.pk)
            par=par.par
        ls=reversed([str(x) for x in ls])
        self.par_chain='.'.join(ls)
        self.save()
        for depart in self.childs.all():
            depart.update_parent_chain() 
    

class Employee(models.Model):
    user = models.ForeignKey(User,verbose_name=_('account'), blank=True, null=True)
    eid=models.CharField(_('employee id'),max_length=30,default='')    
    baseinfo=models.OneToOneField(BasicInfo,verbose_name=_('basic info'),blank=True,null=True)
    position = models.CharField(_('job position'),max_length=100,blank=True)
    depart=models.ForeignKey(Department,verbose_name=_('department'),blank=True,null=True,on_delete=models.SET_NULL)

    class Meta:
        verbose_name=_('Employee Info')



