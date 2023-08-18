from django.db.models.base import ModelBase
from django.db import models

class OrmBase(ModelBase):
    def __new__(cls, name, bases, namespace):
        """
        新建类的时候调用
        """
        print('Singleton new')  
 
        base = bases[0]

        for ii in base._meta.fields:
            if ii.name not in namespace:
                if namespace.get('_base_include'):
                    if ii.name not in namespace.get('_base_include'):
                        continue
                elif namespace.get('_base_exclude'):
                    if ii.name in namespace.get('_base_exclude'):
                        continue  
                namespace[ii.name] = ii
                #setattr(cls,ii.name,ii)
                #cls[ii.name] = ii
  
        
        return super().__new__(cls, name, (models.Model,), namespace)
        
    #def __init__(self, *args, **kwargs):
        #"""
        #新建类后，初始化，调用该函数
        #"""
        #print('Singleton init')
        #self._instance = None
        #super().__init__(*args, **kwargs)

    #def __call__(self, *args, **kwargs):
        #"""
        #用类创建instance的时候，调用该函数。。这个函数完了之后，才回调用 instance.__init__
        #这里控制单例模式
        #"""
        #print('Singleton call')
        #if self._instance is None:
            #self._instance = super().__call__(*args, **kwargs)
            #return self._instance
        #else:
            #return self._instance

#class Base1(object):
    #name = 'my name is base1'

#class Spam(Base1,metaclass=OrmBase):
    #name='dog'
    #def __init__(self):
        #print("Spam!!!")

