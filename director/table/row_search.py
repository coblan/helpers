
from django.utils.translation import ugettext as _
from helpers.director.base_data import field_map
from django.db.models import Q
from helpers.director.model_func.dictfy import model_to_name
from django.core.exceptions import FieldDoesNotExist

class SelectSearch(object):
    names=[]
    exact_names = []
    model=''
    field_sort=[]
    orders = {}  # 字段排序，小的排在前面
    
    db_map={} # 用户 raw sql 查询时，映射字段到 数据库字段
    label_map = {} # name 到 label 的映射
    def __init__(self,q,user = None,allowed_names = [], kw = {}):
        self.crt_user=user
        self.valid_name=  self.names + self.exact_names  #[x for x in self.names if x in allowed_names]
        self._names=[x for x in self.names if x in allowed_names]        
        self.q=q
        self.qf = kw.get('_qf')
        self.kw = kw
         
    def get_context(self):
        """
        """
        sorted_name = []
        if self.field_sort:
            for item in self.field_sort:
                if item in self.valid_name:
                    sorted_name.append(item)
        else:
            sorted_name = sorted( self.valid_name ,key=lambda name:self.orders.get(name,0))
        if sorted_name:
            ls=[]
            for name in sorted_name:
                option = self.get_option(name)
                if name in self.exact_names:
                    option['exact_search'] = True
                ls.append( option )
                #ls.append({'value': name, 'label': _(self.model._meta.get_field(name).verbose_name) })
            dc = {
                'options':ls,
                'editor':'com-search-select',
                'name':'_q'
            }
            return dc
        
    def get_option(self, name): 
        if self.label_map.get(name):
            return {'value':name,'label':self.label_map.get(name)}
        else:
            return {'value': name, 'label': _(self.model._meta.get_field(name).verbose_name) }
    
    def clean_search(self): 
        "可以返回字符串。或者返回字典,直接代入query查询"
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
                query = query.filter(pk = None)
            elif isinstance(q_str,dict):
                query = query.filter(**q_str)
            else:
                exp = self.get_express(q_str)
                query = query.filter(exp)
        custom_exp = self.getFilterArgs()
        if custom_exp:
            query = query.filter(**custom_exp)
        return query
    
    def get_express(self, q_str): 
        exp = None
        if self.qf:
            if self.qf in self.exact_names:
                exp = {self.qf : q_str}
            else:
                exp = {'%s__contains'%self.qf: q_str,}
        else:
            raise UserWarning('没有指定查询字段')
        return Q(**exp)
    
    def getFilterArgs(self,):
        exp = {}
        for ii  in self.names:
            if self.kw.get(ii):
                exp [f'{ii}__contains'] = self.kw.get(ii)
        for ii in self.exact_names:
            if self.kw.get(ii):
                exp[ii] = self.kw.get(ii)
        return exp
    
    def inject_sql(self,where_list,params):
        if self.q and self.qf:
            db_field = self.db_map.get(self.qf,self.qf)
            if self.qf in self.exact_names:
                #where_list.append( '%s = %s'%(db_field,self.q) )
                where_list.append( db_field +" = %s" )
                params.append('%s'%self.q)
            else:
                where_list.append( db_field +" like %s" )
                params.append('%%%s%%'%self.q)
