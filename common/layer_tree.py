# encoding:utf-8

from helpers.director.shortcut import ModelPermit
from helpers.director.db_tools import to_dict,model_to_name,from_dict
from django.core.exceptions import PermissionDenied

"""
>5>comp/catalog.rst>
后端
======
源文件:helpers.commmon.dir_man.py

catalog管理的后台逻辑。一般情况下是后台一个dir数据表，一个item数据表。DirMan类要求：dir和item表中，以外键形式指向dirparent，字段名为 **par**。
DirMan不需要继承，只需要实例化，即可使用。

使用步骤:

1. 构建views函数::

    from helpers.common.dir_man import DirMan
    from .models import Work,Index
    import inspect
    # Create your views here.
    
    def dir_man(request):
        manager=DirMan(Index, Work)
        scope= dict(inspect.getmembers(manager,inspect.ismethod))
        return jsonpost(request, scope)
        
2. 完成url.py路由::

    url(r'^dir_mana',workload_view.dir_man),

这样，前端可以通过改地址，与后端函数群进行通信。
<-<
"""

class LayerTree(object):
    def __init__(self,model):
        self.model=model
        
    def dir_data(self,root,par,user):
        """
        @root: 自定义
        @par: to_dict 对象
        
        return :{'parent':[],'items':[]}
        
        items 是 to_dict对象，为每个对象添加_type 属性，定义前段使用的显示
        """
        if '_class' not in root.keys():
            root=from_dict(root,model=self.model)
        else:
            root=from_dict(root)
        
        parents=[]
        if not par.get('pk',None):
            items=[to_dict(x) for x in self.model.objects.filter(par=None)]
            par=root
        else:
            par=from_dict(par)
            items=[to_dict(x) for x in self.model.objects.filter(par=par)]
        
        crt_par=par
        while True:
            parents.append(crt_par)
            crt_par=crt_par.par
            if not crt_par or not crt_par.pk or crt_par==root:
                break            
        if root not in parents:
            parents.append(root)
        parents.reverse()
        
        return {
            'parents':[to_dict(x)  for x in parents],
            'items':items,
        }
    
        #par_permit=ModelPermit(self.DIR,user)
        #if not par_permit.readable_fields():
            #raise PermissionDenied,'can not read %s'% model_to_name(self.DIR) 
        #DIR=self.DIR
        
        #if self.ITEM:
            #item_perm=ModelPermit(self.ITEM,user)
            #if not item_perm.readable_fields():
                #raise PermissionDenied,'can not read %s'%model_to_name(self.ITEM)
        
            #ITEM=self.ITEM 

        #if par:
            #query = DIR.objects.filter(par_id=par)
        #else:
            #query = DIR.objects.filter(par=None)
        #rows=[to_dict(idx) for idx in query]
        
        #parents=[]
        #if par:
            #this_dir=DIR.objects.get(id=par)
            #parents.append(this_dir)
            #while this_dir.par:
                #parents.append(this_dir.par)
                #this_dir=this_dir.par
        #parents.reverse()
        #parents= [to_dict(idx) for idx in parents]
        #items=[]   # 如果有item_model，才会去查询item项
        #if self.ITEM:
            #if par:
                #items=[to_dict(item,include=item_perm.readable_fields()) for item in ITEM.objects.filter(par_id=par)]
            #else:
                #items=[to_dict(item,include=item_perm.readable_fields()) for item in ITEM.objects.filter(par=None)]
        #return {'dirs':rows,'parents':parents,'items':items}
    
    
    def item_create(self,user,kind,par=None):
        if not ModelPermit(self.DIR,user).can_add():
            raise PermissionDenied,'not permit create %s'%model_to_name(self.DIR)
        
        if not par:
            i = self.DIR.objects.create()
        else:
            i = self.DIR.objects.create( par_id=par)
        return to_dict(i)
    

    
    def items_paste(self,rows,par,user):
        """粘贴 dir 和 item """
        if par:
            par_inst=self.DIR.objects.get(pk=par)
        else:
            par_inst=None
        for row in rows:
            inst = from_dict(row)
            if 'par' in  ModelPermit(inst,user).changeable_fields():
                inst.par=par_inst
                inst.save()
            else:
                raise PermissionDenied,'can not modify par of %s'% model_to_name(inst)
        return {'status':'success'}
     
    def item_del(self,rows,user):
        """ 删除 dir 和 item """
        for row in rows:
            inst=from_dict(row)
            if ModelPermit(inst,user).can_del():
                inst.delete()
            else:
                raise PermissionDenied,'can not delete %s'% model_to_name(inst)
        return {'status':'success'}    