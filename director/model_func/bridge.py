from helpers.director.model_func.dictfy import sim_dict,to_dict
from helpers.director.shortcut import ModelFields,ModelTable
from django.forms.models import ModelFormMetaclass
import re
from helpers.func.dot_dict import read_dict_path

class BridgeTableMeta(type):
    def __new__(cls, name, bases, namespace):
        """
        新建类的时候调用
        """
        foreign_bridge = namespace.get('foreign_bridge')
        base_cls = bases[0]
        model = namespace.get('model')
        if not model:
            model = base_cls.model
        if not foreign_bridge:
            foreign_bridge = [x.copy() for x in  base_cls.foreign_bridge ]
            namespace['foreign_bridge'] = foreign_bridge
        for bridge in foreign_bridge:
            #field = model._meta.get_field(bridge.field_name)
            bridge.updateRelatedModel(model, # field.related_model,
                                      simple_dict=namespace.get('simple_dict',False),
                                      nolimit=namespace.get('nolimit',False))
            
        return super().__new__(cls, name, bases, namespace)
    
    #def __init__(self, *args, **kwargs):
        #"""
        #新建类后，初始化，调用该函数
        #"""
        #super().__init__(*args, **kwargs)
        #org_get_rows = self.get_rows
        #def _get_rows(*args,**kws):
            #rows =  org_get_rows(*args,**kws)
            #for row in rows:
                #pass
            
        #self.get_rows = _get_rows
    
  

class ForeignTableBridge(object):
    def __init__(self,table=None,field_name='',prefix=None,label_prefix='',include=None,related_model=None):
        self.org_tab = table
        self.table = table
        self.field_name= field_name.replace('__','.')
        if not prefix:
            self.prefix = field_name +'__'
        else:
            self.prefix = prefix
        self.label_prefix = label_prefix
        self.related_model = related_model  # 由meta类注入
        self.include=include
    
    def updateRelatedModel(self,model,simple_dict=False,nolimit=False):# 由meta类注入
        """
        @model:main model
        
        [TODO] 遇到多级表join的情况 ,现在 related_model是用的外部直接传入的，不能自动生成。
        """
        if not self.related_model:
            field = model._meta.get_field(self.field_name)
            self.related_model = field.related_model
        if not self.table:
            class _table(ModelTable):
                model = self.related_model   
                exclude =[]
                include=self.include
            self.table = _table
        self.table.simple_dict = simple_dict
        self.table.nolimit = nolimit
    
    def copy(self):
        return ForeignTableBridge(self.org_tab,self.field_name,self.prefix,self.label_prefix)
    
    def parseDict(self):
        pass
    
    def getHeads(self):
        heads = self.table().get_heads()
        out_heads = [] 
        for head in heads:
            if head['name'] in ['pk','id']:
                continue            
            head['name'] = self.prefix + head['name']
            head['label'] = self.label_prefix+head['label']
            out_heads.append(head)
        return out_heads
    
    def getRow(self,inst):
        out_dc = {}
        #if hasattr(inst,self.field_name):
        if read_dict_path(inst,self.field_name):
            base_inst = read_dict_path(inst,self.field_name)
            if not base_inst:
                return {}
            dc= self._getRow(base_inst)
            for k,v in dc.items():
                if k in ['pk','id']:
                    continue
                mt =  re.search('^_(\w+)_label',k)
                if mt:
                    out_dc[f'_{self.prefix}{mt.group(1)}_label']=v
                else:
                    out_dc[f'{self.prefix}{k}'] =v
                
        return out_dc
    
    def _getRow(self,base_inst):
        table_inst = self.table()
        cus_dict = table_inst.dict_row( base_inst)
        permit_fields =  table_inst.permited_fields()
        include_pk = True
        if self.include:
            permit_fields = [ x for x in self.include if x in permit_fields]
            if 'pk' not in self.include:
                include_pk =False
                
        if table_inst.simple_dict:
            dc = sim_dict(base_inst, include=permit_fields,filt_attr=cus_dict,include_pk=include_pk) # include_pk=False
        else:
            dc= to_dict(base_inst, include=permit_fields,filt_attr=cus_dict,include_pk=include_pk)
            dc .update({
                f'_director_name':table_inst.get_edit_director_name(),
                f'meta_org_dict':table_inst.get_org_dict(dc,base_inst)
                })
        # 再赋值一次，以免被默认dictfy替换掉了，例如 _x_label等        值
        dc.update(cus_dict)
        return dc



class BridgeFormMeta(ModelFormMetaclass):
    def __new__(cls, name, bases, namespace):
        """
        新建类的时候调用
        """
        foreign_bridge = namespace.get('foreign_bridge')
        base_cls = bases[0]
        meta = namespace.get('Meta')
        if not meta:
            meta = base_cls._meta
        model = meta.model

        if not foreign_bridge:
            foreign_bridge = [x.copy() for x in  base_cls.foreign_bridge ]
            namespace['foreign_bridge'] = foreign_bridge
        for bridge in foreign_bridge:
            field = model._meta.get_field(bridge.field_name)
            bridge.updateRelatedModel(field.related_model,
                                      simple_dict=namespace.get('simple_dict',False),
                                      nolimit=namespace.get('nolimit',False))
            
        return super().__new__(cls, name, bases, namespace)

class ForeignFormBridge(ForeignTableBridge):
    def __init__(self,field_name,form=None,prefix=None,label_prefix='',):
        #if not form:
            #class _form(ModelFields):
                #class Meta:
                    #model = 
        self.org_form = form
        self.form = form
        self.field_name= field_name
        if not prefix:
            self.prefix = field_name +'__'
        else:
            self.prefix = prefix
        self.label_prefix = label_prefix
        self.related_model = None   # 由metaclass类注入
 
    
    def copy(self):
        return self.__class__(self.field_name,form=self.org_form,prefix=self.prefix,label_prefix=self.label_prefix)
        #return ForeignFormBridge(self.field_name,form=self.org_form,prefix=self.prefix,label_prefix=self.label_prefix)
    
    def updateRelatedModel(self,model,simple_dict=False,nolimit=False):# 由metaclass类注入
        self.related_model = model
        if not self.form:
            class _form(ModelFields):
                class Meta:
                    model = self.related_model   
                    exclude =[]
            self.form = _form
        self.form.simple_dict = simple_dict
        self.form.nolimit = nolimit    
    
    def parseDict(self, dc,base_inst,crt_user,select_for_update,*args,**kw):
        """
        分解前端传来的字段
        
        """
        real_dc = {}
        for k in dc:
            if k.startswith(self.prefix):
                key = k[len(self.prefix):]
                real_dc[key] = dc[k]
        out_kw = dict(kw)
        if hasattr(base_inst,self.field_name):
            instance = getattr(base_inst,self.field_name)
            if instance:
                out_kw['instance'] = instance
        return self.form(real_dc,pk=None,crt_user=crt_user,select_for_update=select_for_update,*args,**out_kw)
    
    def getHeads(self,bridge_inst,base_inst):
        heads = self.form().get_heads()
        for head in heads:
            head['name'] = self.prefix + head['name']
            head['label'] = self.label_prefix+head['label']
        return heads
    
    def isValid(self,bridge_inst):
        return bridge_inst.is_valid()
    
    def getErrors(self,bridge_inst):
        errors =  bridge_inst.get_errors()
        dc = {}
        for k,v in errors.items():
            dc[self.prefix+k]=v
        return dc
    
    def saveForm(self,bridge_inst,base_inst):
        bridge_inst.save_form()
        setattr(base_inst,self.field_name,bridge_inst.instance)
    
    def getRow(self,bridge_inst):
        """
        """
        row = bridge_inst.get_row()
        out_dc = {}
        for k,v in row.items():
            if k in ['pk','id']:
                continue            
            mt =  re.search('^_(\w+)_label',k)
            if mt:
                out_dc[f'_{self.prefix}{mt.group(1)}_label']=v   
            else:
                out_dc[f'{self.prefix}{k}'] =v
        return out_dc
    
    def joinRow(self,bridge_inst:ModelFields,left_row):
        """
        modelfields类调用，传递bridge_inst,父row进来
        """
        right_row = self.getRow(bridge_inst) 
        if self.field_name in left_row:
            del left_row[self.field_name]
        if f'_{self.field_name}_label' in left_row:
            del left_row[f'_{self.field_name}_label']
        if f'_{self.field_name}_model' in left_row:
            del left_row[f'_{self.field_name}_model'] 
        left_row.update(right_row)
        
            
    
    def delForm(self,bridge_inst,base_inst):
        """一般来说都是连带删除"""
        bridge_inst.del_form()

class SelectForeignFormBridge(ForeignFormBridge):
    #def copy(self):
        #return SelectForeignFormBridge(self.field_name,form=self.org_form,prefix=self.prefix,label_prefix=self.label_prefix)
    
    def parseDict(self, dc,base_inst,crt_user,select_for_update,*args,**kw):
        """
        分解前端传来的字段
        """
        #if dc.get(self.field_name):
            
        real_dc = {}
        for k in dc:
            if k.startswith(self.prefix):
                key = k[len(self.prefix):]
                real_dc[key] = dc[k]
        
        real_kw = {}
        for k in kw:
            if k.startswith(self.prefix):
                key = k[len(self.prefix):]
                real_kw[key] = kw[k]        
        #out_kw = dict(kw)
        if hasattr(base_inst,self.field_name):
            instance = getattr(base_inst,self.field_name)
            if instance:
                real_kw['instance'] = instance
        #real_dc = {}
        pk = dc.get(self.field_name)
        return self.form(real_dc,pk=pk,crt_user=crt_user,select_for_update=select_for_update,*args,**real_kw)
    
    def isValid(self, bridge_inst):
        return True
    
    def saveForm(self,bridge_inst,base_inst):
        pass
        #bridge_inst.save_form()
        #setattr(base_inst,self.field_name,bridge_inst.instance)
        
    def joinRow(self,bridge_inst:ModelFields,left_row):
        """
        modelfields类调用，传递bridge_inst,父row进来
        """
        right_row = self.getRow(bridge_inst) 
        left_row.update(right_row)