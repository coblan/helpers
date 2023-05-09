# encoding:utf-8
from ..field_proc  import BaseFieldProc
from django.db.models import ForeignKey,OneToOneField
from django.core.exceptions import ObjectDoesNotExist
from .. .base_data import field_map
from django.utils.translation import ugettext as _
from ..dictfy  import model_to_name,name_to_model
from helpers.director.middleware.request_cache import get_request_cache
#from pypinyin import lazy_pinyin
from helpers.director.model_func.cus_fields.compositefk.fields import CompositeForeignKey

class ForeignProc(BaseFieldProc):
    def to_dict(self,inst,name):
        try:
            foreign=getattr(inst,name,None)
        except ObjectDoesNotExist:
            foreign = None
            
        if foreign:
            return {
                name:  getattr(inst,name + '_id', '') , #foreign.pk,
                #'_%s_model'%name:model_to_name(foreign.__class__),
                '_%s_label'%name:str(foreign)
            }
        else:
            return {
                name:  getattr(inst,name + '_id', None), # foreign,
                '_%s_label'%name: getattr(inst,name + '_id', '')                
            }
    def get_options(self):
        if getattr(self.field.target_field.model,'bigdata',False):
            return [{'value':0,'label':'大数据量,请自定义'}]        
        else:
            return super().get_options()
    
    # 外键不能转换为对象，直接用pk值就行。
    #def clean_field(self,dc,name):
    
        #model = name_to_model( dc.get('_%s_model'%name) )
        #return model.objects.get(pk=dc.get(name))     
    
    def dict_table_head(self, head): 
        head['editor'] = 'com-table-label-shower'
        head['options']=[]
        return head
    
    def filter_get_head(self, name, model):
        this_field= model._meta.get_field(name)
        if getattr(self.field.target_field.model,'bigdata',False):
            options =  [{'value':0,'label':'大数据量,请自定义'}]
        else:  
            
            catch = get_request_cache()
            option_name = model_to_name(model)+'.%s.options'%name
            
            if not catch.get(option_name):
                def mychoice_func():
                    ls=this_field.get_choices()
                    ls=ls[1:]
                    options = [{'value':x[0],'label':x[1]} for x in ls] 
                    #options=sorted(options,key=lambda item: ''.join(lazy_pinyin(item.get('label'))) )
                    catch[option_name] = options
                    return options
                options= mychoice_func  
                
            else:
                options = catch.get(option_name)
        return {
            'name':name,
            'label':_(this_field.verbose_name),
            'editor': 'com-filter-select',
            'options':options
        }        


field_map.update({
    ForeignKey:ForeignProc,
    OneToOneField:ForeignProc,
    CompositeForeignKey:ForeignProc,
})