# encoding:utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
#from core.db_tools import to_dict,model_to_head,model_stringfy
import json
from django.db.models import Q,fields
from django.core.exceptions import PermissionDenied
from ..access.permit import ModelPermit
from ..model_func.dictfy import model_to_name,to_dict,model_to_head,model_to_name,model_dc,field_map
from django.db import models
import math
import time
from django.conf import settings
from helpers.director.base_data import director
#import pinyin
#from forms import MobilePageForm


from django.core.paginator import Paginator


class PageNum(object):
    perPage=20
    def __init__(self,pageNumber=1,perpage=None,kw={}):
        self.pageNumber = int(pageNumber)
        if perpage:
            self.perPage= int(perpage)
        
    
    def get_query(self,query):
        #count = query.count()
        #totalpage = int( math.ceil( float( count )/self.perPage) )
        #self.totalpage = max(totalpage,1)
        
        #self.query = query  
        #crt_page=min(self.totalpage,abs(int( self.pageNumber)))
        #start = (crt_page -1)*self.perPage
        #end = min(crt_page*self.perPage,count)
        #return query[start:end]
        self.pagenator = Paginator(query,self.perPage)
        self.pageNumber = min(self.pagenator.num_pages,abs(int( self.pageNumber)))
        return self.pagenator.page(self.pageNumber)
        #return self.pagenator.page(self.pageNumber)
        
        
    
    def get_context(self):
        """
        rt: {'options':[1,2,3,4,...,100],
             'crt_page':2
            }
        """
        #choice_len = len(self.pagenator.page_range)
        #k=3
        #a=-1
        #while a < 1:
            #a=self.pageNumber-k
            #k-=1
        #page_nums = range(a,min(choice_len,self.pageNumber+(5-k))+1)
        #if page_nums[0] != 1:
            #page_nums=[1,'...']+ page_nums
        #if page_nums[-1] != choice_len:
            #page_nums = page_nums +['...',choice_len]
        #for i in range(len(page_nums)):
            #num = page_nums[i]
        #page_nums=[str(x) for x in page_nums]

        #return {'options':page_nums,'crt_page':self.pageNumber}    
        return {'crt_page':self.pageNumber,
                'total':self.pagenator.count,
                'perpage':self.perPage}

class TrivalPageNum(object):
    def __init__(self,pageNumber=1,kw={}):
        pass    
    def get_query(self,query):
        return query
    def get_context(self):
        return {}
    

class RowSearch(object):
    names=[]
    model=''
    def __init__(self,q,user,allowed_names,kw={}):
        self.valid_name=[x for x in self.names if x in allowed_names]
        self.crt_user=user
        self._names=[x for x in self.names if x in allowed_names]        
        self.q=q
        #for k in self.names:
            #v = dc.pop(k,None)
            #if v:
                #self.search_args[k]=v
         
    def get_context(self):
        """
        """
        if self.valid_name:
            ls=[]
            for name in self.valid_name:
                ls.append(_(self.model._meta.get_field(name).verbose_name) )
            dc = {
                'search_tip':','.join(ls),
                'editor':'com-search-filter',
                'name':'_q'
            }
            return dc
    
    def get_query(self,query):
        if self.q:
            exp=None
            for name in self.valid_name:
                kw ={}
                kw['%s__icontains'%name] =self.q    
                if exp is None:
                    exp = Q(**kw)
                else:
                    exp = exp | Q(**kw) 
            return query.filter(exp)
        else:
            return query

class RowFilter(object):
    """
    @names : 普通字段，用于过滤用.
    @range_fields: span字段，例如时间段
    
     range_fields=[{'name':'create_time','type':'date'}]
    """
    names=[]
    range_fields=[]
    model=''
    def __init__(self,dc,user,allowed_names,kw={}):
        self.names = self.names + self.range_fields #+ [x.get('name') for x in self.range_fields]
        self.valid_name=[x for x in self.names if x in allowed_names]
        self.crt_user=user
        #self._names=[x for x in self.names if x in allowed_names]        
        self.filter_args={}
        for k in self.names:
            v = dc.pop(k,None)
            if v != None:
                self.filter_args[k]=v   
            if v=='0':
                self.filter_args[k]=False
            elif v=='1':
                self.filter_args[k]=True
        for k in self.range_fields: #[x.get('name') for x in self.range_fields]:
            if kw.get('_start_%s'%k):
                start=kw.get('_start_%s'%k)
                self.filter_args['%s__gte'%k]=start
            if kw.get('_end_%s'%k):
                end=kw.get('_end_%s'%k)
                self.filter_args['%s__lte'%k]=end            
    
    def get_proc_list(self):
        ls=[]
        for name in self.valid_name:
            
            # 先查找 proc
            model_name = model_to_name(self.model)
            model_field_name = '%s.%s'%(model_name,name)
            proc_cls =field_map.get(model_field_name)
            
            if not proc_cls:
                f = self.model._meta.get_field(name)
                proc_cls  =field_map.get(f.__class__)            
            ls.append(proc_cls)
        return ls
    
    def get_context(self):
        ls=[]
        for proc_cls,name in zip(self.get_proc_list() ,self.valid_name):

            if name in self.range_fields:
                
                filter_head = proc_cls().filter_get_range_head(name,self.model)
                ls.append(filter_head)
  
            else:
                filter_head = proc_cls().filter_get_head(name,self.model)
                ls.append(filter_head)
                
        return ls
      
    def get_query(self,query):
        self.query=query
        dc = {}
        for proc_cls,name in zip(self.get_proc_list() ,self.valid_name):
            dc.update( proc_cls().filter_dict_query_args(self.filter_args, name ) )
        self.filter_args.update(dc)
        query=query.filter(**self.filter_args)
        return query    
    
  
    
    
class RowSort(object):
    """
    row_sort: 'name1,-name2'
    """
    names=[]
    chinese_words=[]
    def __init__(self,row_sort=[],user=None,allowed_names=[],kw={}):
        self.valid_name=[x for x in self.names if x in allowed_names]
        ls=[]
        for x in row_sort:
            if x.lstrip('-') in self.valid_name:
                ls.append(x)
        self.sort_str=','.join(ls)
        
    def get_context(self):
        return {'sortable':self.valid_name,'sort_str':self.sort_str}
    
  
    
    def get_query(self,query):
        if self.sort_str:
            ls=self.sort_str.split(',')
            for name in ls:
                if name.startswith('-'):
                    norm_name=name.lstrip('-')
                    direction='-'
                else:
                    norm_name=name
                    direction=''                    
                if norm_name in self.chinese_words:
                    engine= settings.DATABASES.get(query.db)['ENGINE'] 
                
                    if engine == 'django.contrib.gis.db.backends.postgis':
                        # postgresql 注意，postgre的默认中文排序，好像是按照拼音来的（如果这样的话，下面这句程序就没用了。），待以后确认
                        query= query.extra(select={'converted_%s'%norm_name: "convert_to(%s,'GBK')"%norm_name},order_by=['%sconverted_%s'%(direction,norm_name)])
                    else:
                        # mysql 按照拼音排序
                        query= query.extra(select={'converted_%s'%norm_name: 'CONVERT(%s USING gbk)'%norm_name},order_by=['%sconverted_%s'%(direction,norm_name)])                        
                else:
                    query= query.order_by(name)

        return query

  
class ModelTable(object):
    """
    
    Getter Method:
    ===============
    get_heads(self):
        return [{name:'xxx',label:'xxx',sortable:true}]
        
    get_rows(self):
        return [{}]
    

    over-load Method:
    =================
    inn_filter(self,query):
        process inn filter logic . Get gid of ,Ex: user-ware ,group-ware data.
        these data will be used for sort and filter in front-end
        
    """
    model=''
    sort=RowSort
    search=RowSearch
    filters=RowFilter
    include=None
    exclude=[]
    hide_fields = []
    pagenator=PageNum
    fields_sort=[]
    pop_edit_field=""
    def __init__(self,_page=1,row_sort=[],row_filter={},row_search= '',crt_user=None,perpage=None,**kw):
        self.search_args = kw.get('search_args')
        
        self.kw=kw
        self.crt_user=crt_user 
        self.page=_page
        
        self.custom_permit()
        allowed_names=self.permited_fields()
        
        self.row_sort=self.sort(row_sort,crt_user,allowed_names,kw)
        self.row_filter=self.filters(row_filter, crt_user, allowed_names,kw) 
        self.row_search = self.search( row_search,crt_user,allowed_names,kw)
        if not self.row_filter.model:
            self.row_filter.model=self.model
        if not self.row_search.model:
            self.row_search.model=self.model
        self.pagenum = self.pagenator(pageNumber=self.page,perpage=perpage)
        
        
        
    
    def custom_permit(self):
        self.permit=ModelPermit(model=self.model, user=self.crt_user)

    @classmethod
    def parse_request(cls,request):
        """
        传入参数的形式：
        row_search: key=value&..
        row_sort: _sort=key1,-key2
        page: _page=1
        row_filter:key=value&..
        """
        kw = request.GET.dict()
        return cls.gen_from_search_args(kw,request.user)

    @classmethod
    def gen_from_search_args(cls,search_args,user):
        args = cls.clean_search_args(search_args)
        kw = dict(args)
        kw['search_args'] = args
        page = kw.pop('_page','1')
        perpage = kw.pop('_perpage',None)
        row_sort = kw.pop('_sort','').split(',')
        row_sort=filter(lambda x: x!='',row_sort)
        q=kw.pop('_q',None)
        row_filter={}
        for k in cls.filters.names:
            arg = kw.pop(k,None)
            if arg is not None:
                row_filter[k]=arg
        return cls(page,row_sort,row_filter,q,user,perpage=perpage,**kw)
    
    @classmethod
    def clean_search_args(cls,search_args):
        """
        重载该函数，用于调整search_args的默认值，修改值
        返回的参数 (1,2) 1用于传入 filter ，2 用于传回前端去显示。
        
        例如对于类型为datetime的filter，
        _end_xxx = 2018-10-23  传到filter的值为 _end_xxx=2018-10-24 ,传到前端的值为 _end_xxx=2018-10-23
        """
        args=dict(search_args)
        return args
    
    @classmethod
    def get_director_name(cls):
        director_name = ''
        for k,v in director.items():
            if v==cls: # self.__class__:
                director_name=k
                break
        return director_name
    
    def get_context(self):
        ls=[]
        search_head = self.row_search.get_context()
        row_filters = self.row_filter.get_context()
        # 合并search和rowfilter 为rowfilter
        if search_head:
            ls.append( search_head)
        if row_filters:
            ls.extend(row_filters)
        
        director_name =self.get_director_name()
        return {
            'heads':self.get_heads(),
            'rows': self.get_rows(),
            'row_pages' : self.pagenum.get_context(),
            'row_sort':self.row_sort.get_context(),
            'row_filters':ls,
            #'search_tip':self.row_search.get_context(),
            'director_name':director_name,
            'model_name':model_to_name(self.model),
            'ops' : self.get_operation(),
            'search_args':self.search_args
        }
    
    def get_head_context(self):
        """
        有些时候，最先不需要返回rows，而只返回filters，head等，等待用户选择后，才返回rows
        """
        ls=[]
        search_head = self.row_search.get_context()
        row_filters = self.row_filter.get_context()
        # 合并search和rowfilter 为rowfilter
        if search_head:
            ls.append( search_head)
        if row_filters:
            ls.extend(row_filters)
        return {
            'heads':self.get_heads(),
            'rows': [], #self.get_rows(),
            'row_pages':{}, # self.pagenum.get_context(),
            'row_sort':self.row_sort.get_context(),
            'row_filters': ls , #self.row_filter.get_context(),
            #'search_tip':self.row_search.get_context(),
            'director_name': self.get_director_name(),#model_to_name(self.model),
            'ops' : self.get_operation()
        }        
    

    def get_data_context(self):
        return {
            'rows': self.get_rows(),
            'row_pages' : self.pagenum.get_context(),  
            'search_args':self.search_args
        }
    
    def permited_fields(self):
        ls = self.permit.readable_fields()
        
        if 'id' not in self.exclude and 'id' not in ls:
            ls.insert(0,'id')
        elif 'id' in self.exclude and 'id' in ls:
            ls.remove('id')
            
        if self.include:
            return [x for x in self.include if x in ls]
        if self.exclude:
            return [x for x in ls if x not in self.exclude]
        return ls
    
    def getExtraHead(self):
        return []
    
    def get_heads(self):
        """
        return:[{"name": "name", "label": "\u59d3\u540d"}, {"sortable": true, "name": "age", "label": "\u5e74\u9f84"}]
        """
        ls = self.permited_fields()   
        ls = [x for x in ls if x not in self.hide_fields]
        heads = model_to_head(self.model,include=ls)
        heads=[self.fields_map_head(head) for head in heads]
        
        heads.extend(self.getExtraHead())
        heads = self.fields_sort_heads(heads)   
        
        heads= self.make_pop_edit_field(heads)
              
        heads = [self.dict_head(head) for head in heads]
        
        return heads
    
    def make_pop_edit_field(self,heads):
        """
        确定弹出框 列
        """
        if self.pop_edit_field:
            for head in heads:
                if head['name']==self.pop_edit_field:
                    director_name = self.get_director_name()
                    #model_form = model_dc[self.model].get('fields')
                    model_form = director.get(director_name+'.edit')
                    form_obj = model_form(crt_user=self.crt_user)
                    #head['name'] ==self.pop_edit_field
                    head['editor'] = 'com-table-pop-fields'
                    head['fields_ctx']=form_obj.get_head_context()
                    head['get_row'] = {
                        #'fun':'use_table_row'
                        "fun":'get_table_row'
                        #'fun':'get_with_relat_field',
                        #'kws':{
                            #"model_name":model_to_name(TbBanner),
                            #'relat_field':'pk'
                        #}
                    }
                    head['after_save']={
                        #'fun':'do_nothing'
                        'fun':'update_or_insert'
                    }
                    head['ops']=form_obj.get_operations()
                    head['extra_mixins']=form_obj.extra_mixins
        return heads
    
    def dict_head(self,head):
        return head
    
    def fields_map_head(self,head):
        """
        fieldproc 处理
        """
        field = self.model._meta.get_field(head['name'])
        if field.choices:
            head['options']=dict(field.choices)
            head['editor']='com-table-mapper'
        elif isinstance(field,models.BooleanField):
            head['editor']='com-table-bool-shower'
        return head

    def fields_sort_heads(self,heads):
        if not self.fields_sort:
            return heads
        
        tmp_heads = []
        for k in self.fields_sort:
            for head in heads:
                if head['name'] == k:
                    tmp_heads.append(head)
                    #heads.remove(head)
                    break
        #tmp_heads.extend(heads)
        return tmp_heads
            
    def get_rows(self):
        """
        return: [{"name": "heyul0", "age": "32", "user": null, "pk": 1, "_class": "user_admin.BasicInfo", "id": 1}]
        """
        query=self.get_query()
        out=[]
        director_name = self.get_director_name()
        for inst in query:
            # 遇到一种情况，聚合时，这里的queryset返回的item是dict。所以下面做一个判断
            if isinstance(inst,models.Model):
                dc= to_dict(inst, include=self.permited_fields(),filt_attr=self.dict_row( inst))
            else:
                dc = inst
            dc['_director_name'] = director_name+'.edit'
            out.append(dc)
        return out
    

    
    def dict_row(self,inst):
        """
        重写该函数，定制row输出字典
        """
        return {}
    
    def get_query(self):
        if not self.crt_user.is_superuser and not self.permit.readable_fields():
            raise PermissionDenied('no permission to browse %s'%self.model._meta.model_name)
        
        query = self.inn_filter(self.model.objects.all())
        query=self.row_filter.get_query(query)
    
        query=self.row_search.get_query(query)
        query = self.statistics(query)
        query = self.row_sort.get_query(query)
        query = self.pagenum.get_query(query)  
        return query
    
    def statistics(self,query):
        return query
    
    
    def inn_filter(self,query):
        return query.order_by('-pk')
    
    def get_operation(self):
        director_name = self.get_director_name()
        #model_form = model_dc[self.model].get('fields')
        fieldCls = director.get(director_name+'.edit')     
        if not fieldCls:
            return []
        #if not model_dc.get(self.model) or not model_dc.get(self.model).get('fields'):
            #return []
        #model_name =model_to_name(self.model)
           
        #fieldCls=model_dc[self.model].get('fields')
        fieldobj=fieldCls(crt_user=self.crt_user)
        return [{'name':'add_new',
                 'editor':'com-op-btn',
                 'icon': 'fa-plus',
                 'label':'创建',
                 'fields_ctx':fieldobj.get_head_context(),
                 },
                {'name':'save_changed_rows','editor':'com-op-btn','label':'保存','hide':'!changed','icon':'fa-save'},
                {'name':'delete','editor':'com-op-btn','label':'删除','style': 'color:red','icon': 'fa-times','disabled':'!has_select'},
                ]      
    
    #def search_filter(self,query):
        #return self.row_search.get_query(query)
        #for field in self.search_fields:
            #kw ={}
            #kw['%s__icontains'%field] =self.row_search            
        #return query
    
    #def sort_filter(self,query):
        
        #return query
    
    #def out_filter(self,query):
        #if self.search_fields and self.row_search:
            #exp = None
            #for field in self.search_fields:
                #if isinstance(field,SearchQuery):
                    #query=field.get_query(query,self.row_search,self.crt_user)
                #else:
                    #kw ={}
                    #kw['%s__icontains'%field] =self.row_search
                    #if exp is None:
                        #exp = Q(**kw)
                    #else:
                        #exp = exp | Q(**kw)
            #if exp:
                #query= query.filter(exp)
        #if self.row_sort:
            #return query.filter(**self.row_filter).order_by(*self.row_sort)
        #else:
            #return query.filter(**self.row_filter)
    
    #def get_options(self):
        #query = self.inn_filter(self.model.objects.all())
        #options=[]
        #for name in self.filters:
            #tmp = []
            #option =[]
            #field = self.model._meta.get_field(name)
            #label = field._verbose_name
            #value = self.row_filter.get(name,'')
            #for x in query: # get rid of duplicated row
                #if getattr(x,name) not in tmp:
                    #tmp.append(getattr(x,name))
                    #if value == getattr(x,name):
                        #option.append({'label': '%s:%s'%(name,getattr(x,name)),'name':getattr(x,name)})
                    #else:
                        #option.append({'label': getattr(x,name),'name':getattr(x,name)})
            #options.append({
                #'name':name,
                #'label':label,
                #'value': value,
                #'options':option,
            #})
        #return options    
    
    #def get_placeholder(self):
        #ls=[]
        #for field in self.search_fields:
            #if isinstance(field,SearchQuery):
                #ls.append(field.get_placeholder())
            #else:
                #ls.append(self.model._meta.get_field(field).verbose_name)
        #return ','.join(ls)
        # return ','.join([self.model._meta.get_field(name).verbose_name for name in self.search_fields])



# from models import MobilePage
# class PageTable(ModelTable):
    # model = MobilePage
    # sortable=['name','label']
    # filters = ['name','label']
    # include= ['name','label']
    # search_fields=['name']
    # per_page=2
  