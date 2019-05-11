
from django.utils.translation import ugettext as _
from helpers.director.base_data import field_map
from django.db.models import Q
from helpers.director.model_func.dictfy import model_to_name
from django.core.exceptions import FieldDoesNotExist

class SelectSearch(object):
    names=[]
    exact_names = []
    model=''
    def __init__(self,q,user = None,allowed_names = [], kw = {}):
        self.valid_name=  self.names + self.exact_names  #[x for x in self.names if x in allowed_names]
        self.crt_user=user
        self._names=[x for x in self.names if x in allowed_names]        
        self.q=q
        self.qf = kw.get('_qf')
         
    def get_context(self):
        """
        """
        if self.valid_name:
            ls=[]
            for name in self.valid_name:
                ls.append( self.get_option(name) )
                #ls.append({'value': name, 'label': _(self.model._meta.get_field(name).verbose_name) })
            dc = {
                'options':ls,
                'editor':'com-search-select',
                'name':'_q'
            }
            return dc
        
    def get_option(self, name): 
        return {'value': name, 'label': _(self.model._meta.get_field(name).verbose_name) }
    
    def clean_search(self): 
        
        field_path = '%s.%s'%(model_to_name(self.model),self.qf)
        mapper = None
        if field_path in field_map:
            mapperCls = field_map[field_path]
            mapper = mapperCls(name=self.qf,model = self.model)
        else:
            try:
                f = self.model._meta.get_field(self.qf)
                if f:
                    mapperCls = field_map.get(f.__class__)
                    mapper = mapperCls(name=f.name,model = f.model)
            except FieldDoesNotExist:
                pass
           
        if mapper:
            q_str = mapper.filter_clean_search(self.q)
        else:
            q_str = self.q
        return q_str
    
    def get_query(self,query):
        if self.q and self.qf:
            q_str = self.clean_search()
            if q_str == None:
                # 相当于 清空查询集
                return query.filter(pk = None)
            exp = self.get_express(q_str)
            if exp:
                return query.filter( exp)
        return query
    
    def get_express(self, q_str): 
        exp = None
        if self.qf in self.names:
            exp = {'%s__icontains'%self.qf: q_str,}
        elif self.qf in self.exact_names:
            exp = {self.qf : q_str}
        return Q(**exp)
