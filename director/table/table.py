# encoding:utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
#from core.db_tools import to_dict,model_to_head,model_stringfy
import json
from django.db.models import Q,fields
from django.core.exceptions import PermissionDenied
from ..access.permit import ModelPermit
from ..model_func.dictfy import model_to_name,to_dict,model_to_head,model_to_name,model_dc,field_map,sim_dict
from django.db import models
import math
import time
from django.conf import settings
from helpers.director.base_data import director
from django.core.exceptions import FieldDoesNotExist
from helpers.director.middleware.request_cache import get_request_cache,request_cache
from helpers.director.model_func.field_proc import BaseFieldProc
from helpers.func.collection.container import evalue_container
from helpers.director.model_func.hash_dict import make_mark_dict

from django.core.paginator import Paginator
from django.forms.models import fields_for_model
from helpers.director.exceptions.unauth401 import UnAuth401Exception
from django.db import connections
from django.db.utils import ProgrammingError
from helpers.director.model_func.func import str_lazy_label
from helpers.func.collection.ex import findone,find_index
from helpers.case.jb_admin.uidict import pop_edit_current_row


class PageNum(object):
    perPage=20
    def __init__(self,pageNumber=1,perpage=None,**kws):
        self.pageNumber = int(pageNumber)
        if perpage:
            self.perPage= int(perpage)
        
    
    def get_query(self,query,countQuery=None):
        #count = query.count()
        #totalpage = int( math.ceil( float( count )/self.perPage) )
        #self.totalpage = max(totalpage,1)
        
        # 需要研究下，为什么有时 len(query) != query.count()  ，例如 jb.maindb.ticket_admin.TicketparlayTable
        if countQuery==None:
            self.count = query.count()
        else:
            self.count = countQuery.count()
        #crt_page= max(1,int( self.pageNumber))
        #start = (crt_page -1)*self.perPage
        #end = min(crt_page*self.perPage, self.count)
        start,end = self.get_slice_index()
        return query[start:end]
        
        # 这里在某些子查询里面会触发group sql，会报错。所以改成简单方式
        #self.pagenator = Paginator(query,self.perPage)
        #self.pageNumber = min(self.pagenator.num_pages,abs(int( self.pageNumber)))
        #self.count = self.pagenator.count
        #return self.pagenator.page(self.pageNumber)
    
    def get_slice_index(self):
        crt_page= max(1,int( self.pageNumber))
        start = (crt_page -1)*self.perPage
        end = min(crt_page*self.perPage, self.count)
        return start,end
    
    def get_context(self):
        """
        rt: {'options':[1,2,3,4,...,100],
             'crt_page':2
            }
        """
        return {'crt_page':self.pageNumber,
                'total':self.count,
                'perpage':self.perPage}

class TrivalPageNum(object):
    def __init__(self,pageNumber=1,perpage=None,kw={}):
        pass    
    def get_query(self,query):
        return query
    def get_context(self):
        return {}
    

class RowSearch(object):
    names=[]
    model=''
    def __init__(self,q,user = None,allowed_names = [],kw={}):
        self.valid_name= self.names  # [x for x in self.names if x in allowed_names]
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
            field_names = [f.name for f in self.model._meta.get_fields()]
            for name in self.valid_name:
                if name in field_names:
                    ls.append(_(self.model._meta.get_field(name).verbose_name) )
                else:
                    ls.append(name)
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
    
    
     #range_fields=[{'name':'create_time','type':'date'}]
    """
    names=[]   # 该list中的字段，会经过 map cls 正常流程，进行映射。  除了 extrahead中的字段
    range_fields=[]   
    model=''
    fields_sort = [] # 排序直接用names作为顺序，如果有些自定义字段不能出现在names中，就需要用到fields_sort来进行排序了。
    icontains=[]   #  该list中的字段，会处理为 com-filter-text类型
    def __init__(self,dc,user,allowed_names,kw={}):
        # 为了让前端不显示
        self.model_allowed_names =  allowed_names
        self.crt_user=user
        # [todo] 应该把属于 model的字段，利用allowd_names 过滤掉
        self.total_names = self.names + self.range_fields #+ [x.get('name') for x in self.range_fields]
        #self.valid_name= self.names  #[x for x in self.names if x in allowed_names]
        
        #self._names=[x for x in self.names if x in allowed_names]        
        self.filter_args={}
        
        # [compare]过滤组件后端逻辑
        for k in self.total_names:
            compare_name = '_%s_compare'%k
            v = dc.pop(k,'')
            if v and compare_name in kw:
                cv = str( kw.get(compare_name) )
                if cv == '0':
                    self.filter_args[k] =v
                elif cv == '1':
                    self.filter_args['%s__gte'%k] =v
                elif cv == '-1':
                    self.filter_args['%s__lte'%k] =v
            else:
                self.filter_args[k] = v
            #if v != None:
                #self.filter_args[k]=v   
            #if v=='0':
                #self.filter_args[k]=False
            #elif v=='1':
                #self.filter_args[k]=True
        for k in self.range_fields: #[x.get('name') for x in self.range_fields]:
            if kw.get('_start_%s'%k):
                start=kw.get('_start_%s'%k)
                self.filter_args['%s__gte'%k]=start
            if kw.get('_end_%s'%k):
                end=kw.get('_end_%s'%k)
                self.filter_args['%s__lte'%k]=end
        self.kw = kw
    
    def get_proc_list(self):
        ls=[]
        has_model = getattr(self, 'model')
        if has_model:
            field_names = [f.name for f in self.model._meta.get_fields()]
        else:
            field_names = []
        for name in self.total_names:
            # 先查找 proc
            proc_cls = None
            if has_model:
                model_name = model_to_name(self.model)
                model_field_name = '%s.%s'%(model_name,name)
                proc_cls =field_map.get(model_field_name, None)
            
            # 如果不是数据库的字段，就不用去查询了
            if not proc_cls and name in field_names:
                f = self.model._meta.get_field(name)
                proc_cls  =field_map.get(f.__class__)   
            if not proc_cls:
                proc_cls =  BaseFieldProc
            ls.append(proc_cls)
        return ls
    
    def dict_head(self, head): 
        return head
    
    def getExtraHead(self): 
        return []
    
    def get_context(self):
        """
        返回：
        heads=[
           
        ]
        """
        
        extraHead= self.getExtraHead()
        normal_heads = []
        extrahead_dict = {x['name']: x  for x in extraHead }
        valid_model_names = [x for x in self.total_names if x in self.model_allowed_names]
        send_to_front_names = valid_model_names + [x['name'] for x in extraHead]
        
        for proc_cls,name in zip(self.get_proc_list() ,self.total_names):
            if name in extrahead_dict:
                # 为了性能考虑，如果有head了，就不进行自动生成head了，并且排除掉那些不在model里面的字段
                #normal_heads.append(dc[name])
                continue
            
            if name in self.range_fields:
                filter_head = proc_cls(name=name,model=self.model).filter_get_range_head(name,self.model)
                normal_heads.append(filter_head)
  
            else:
                filter_head = proc_cls(name=name,model=self.model).filter_get_head(name,self.model)
                normal_heads.append(filter_head)
        
        out_list = extraHead
        out_list.extend(normal_heads)
        for head in out_list:
            if head['name'] in self.icontains:
                head['editor'] = 'com-filter-text'
                head['options']=[]
        
        out_list = [self.dict_head(head) for head in out_list]
        out_list = [x for x in out_list if x['name'] in send_to_front_names]
        if not self.fields_sort:
            out_list = sorted(out_list, key= lambda x:  self.names.index(x['name']) if x['name'] in self.names else 10000 )
        elif self.fields_sort:
            out_list = [x for x in out_list if x['name'] in self.fields_sort]
            out_list = sorted(out_list, key= lambda x: self.fields_sort.index(x['name']))
        
        out_list = evalue_container(out_list)
        
        return out_list
    
    def clean_query(self, query): 
        return query
    
    def clean_search_args(self,search_args):
        out={}
        for k,v in search_args.items():
            if k in self.icontains:
                out['%s__icontains'%k]=v
            else:
                if v=='true':
                    out[k] = True
                elif v=='false':
                    out[k] = False
                else:
                    out[k]=v
        return out
    
    def get_query(self,query):
        self.query=query
        arg_dc = {}
        for proc_cls,name in zip(self.get_proc_list() ,self.total_names):
            #tmp_dc = proc_cls().filter_clean_filter_arg(name ,self.filter_args )
            proc_cls().filter_clean_filter_arg(name ,self.filter_args )  # 2020/9/17 修改成 有函数 deep 修改 filter_args
            #arg_dc.update( tmp_dc )
            # 由 field_map处理， 移除filter_args的同名字段
            #self.filter_args.pop(name,None)
            #value =  self.filter_args.get(name, None)
            #if value != None:
                #dc[name] = proc_cls().filter_clean_filter_arg(value ) 
        #self.filter_args.update(arg_dc)
        self.filter_args = self.clean_search_args(self.filter_args)
        #arg_dc = {k: v for k, v in self.filter_args.items() if v != None}
        
        query=query.filter(**self.filter_args)
        query = self.clean_query(query)
        return query    
    
    def inject_sql(self,where_list,params):
        pass
    
class RowSort(object):
    """
    row_sort: 'name1,-name2'
    """
    names=[]
    chinese_words=[]
    general_sort='-pk'
    def __init__(self,row_sort=[],user=None,allowed_names=[],kw={}):
        #final_allowd_names = allowed_names + self.extra_allowd_names
        #self.valid_name=[x for x in self.names if x in final_allowd_names]
        self.kw=kw
        self.valid_name=[x for x in self.names]
        ls=[]
        
        for x in row_sort:
            if x.lstrip('-') in self.valid_name:
                ls.append(x)
        self.sort_str=','.join(ls)
        self.clean_search_args()
    
    def clean_search_args(self):
        pass
        
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
                #else:
                    #query = query.order_by(name)
            if self.general_sort:
                ls.append(self.general_sort)
            if ls:
                query = query.order_by(*ls)
        else:
            if self.general_sort =='-pk' and query._fields:
                # 如果query._fields 不为空，代表经过了聚合。默认是pk排序的，这时pk排序会破坏聚合功能。
                query =  query
            elif not query.ordered and self.general_sort:
                norm_name,direction = adapt_field_name(self.general_sort)
                if norm_name in self.chinese_words:
                    query = query_chinese_words(norm_name,direction,query)
                else:
                    query = query.order_by(self.general_sort)

        return query

def query_chinese_words(norm_name,direction,query):
    engine= settings.DATABASES.get(query.db)['ENGINE'] 

    if engine == 'django.contrib.gis.db.backends.postgis':
        # postgresql 注意，postgre的默认中文排序，好像是按照拼音来的（如果这样的话，下面这句程序就没用了。），待以后确认
        query= query.extra(select={'converted_%s'%norm_name: "convert_to(%s,'GBK')"%norm_name},order_by=['%sconverted_%s'%(direction,norm_name)])
    else:
        # mysql 按照拼音排序
        query= query.extra(select={'converted_%s'%norm_name: 'CONVERT(%s USING gbk)'%norm_name},order_by=['%sconverted_%s'%(direction,norm_name)])  
    return query


def adapt_field_name(name):
    if name.startswith('-'):
        norm_name=name.lstrip('-')
        direction='-'
    else:
        norm_name=name
        direction='' 
    return norm_name,direction


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
    pop_edit_fields=[]
    has_sequence = False
    selectable = True
    nolimit = False
    simple_dict = False
    export_related = True
    exclude_export_related =[]  # 有些外键有问题，例如用0作为null，所以这是不用用select_related导出，否则会出现空数据。
    button_edit = False    # 自动添加一列，有一个编辑按钮
    allow_delete = False   # 删除按钮是否显示出来
    check_cascade_delete=True  # 有时让人确认层叠删除很烦，这里可以控制是否提醒用户。
    fitWidth = False
    allow_set_layout = False   # 是否自动打开 设置列。
    allow_create = True # 创建按钮是否显示
    allow_refresh = True
    foreign_bridge = []
    autoLoad = True # 控制前端界面，初始时，是否自动加载。
    def __init__(self,page=1,row_sort=[],row_filter={},row_search= '',crt_user=None,perpage=None,**kw):
        """
        kw['search_args']只是一个记录，在获取到rows时，一并返回前端页面，便于显示。
        而真正的查询参数已经被路由到各个查询组件中，具体参见 cls.parse_request / gen_from_search_args 函数
        如果需要设置查询的默认参数，需要到 cls.clean_search_args中去设置
        
        """
        self.search_args = kw.get('search_args', {})
        
        self.nolimit = kw.get('nolimit',self.__class__.nolimit)
        self.kw=kw
        self.crt_user=crt_user 
        if not self.crt_user:
            self.crt_user = get_request_cache()['request'].user
        self.page= kw.get('_page',page)
        
        self.custom_permit()
        allowed_names=self.permited_fields()
        
        self.row_sort=self.sort(row_sort,self.crt_user,allowed_names,kw)
        self.row_filter=self.filters(row_filter, self.crt_user, allowed_names,kw) 
        self.row_search = self.search( row_search,self.crt_user,allowed_names,kw)
        if not self.row_filter.model:
            self.row_filter.model=self.model
        if not self.row_search.model:
            self.row_search.model=self.model
        myperpage =  self.kw.get('_perpage',perpage)
        self.pagenum = self.pagenator(pageNumber=self.page,perpage=myperpage,table=self)
        # 这个ps暂时不动，但是不能用了。
        self.pagenum.ps = self
        
        self.footer = {}
        self.is_export_excel = False
        self.count_query=None
        
    
    def custom_permit(self):
        self.permit=ModelPermit(model=self.model, user=self.crt_user,nolimit=self.nolimit)

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
        if request.COOKIES.get('advise_heads'):
            kw['_advise_heads'] = kw.get('_advise_heads') or request.COOKIES.get('advise_heads')
        return cls.gen_from_search_args(kw,request.user)

    @classmethod
    def gen_from_search_args(cls,search_args,user =None,**kws):
        args = cls.clean_search_args(search_args)
        kw = dict(args)
        kw['search_args'] = args
        page = kw.pop('_page','1')
        perpage = kw.pop('_perpage',None)
        row_sort = kw.pop('_sort','').split(',')
        row_sort=list( filter(lambda x: x!='',row_sort) )
        q=kw.pop('_q',None)
        #row_filter={}
        #for k in cls.filters.names:
            #arg = kw.pop(k,'')
            #row_filter[k]=arg
        user = user or get_request_cache()['request'].user
        kw.update(kws)
        #return cls(page,row_sort,row_filter,q,user,perpage=perpage,**kw)
        return cls(page,row_sort,kw,q,user,perpage=perpage,**kw)
    
    @classmethod
    def clean_search_args(cls,search_args):
        """
        重载该函数，用于调整search_args的默认值，
        修改值
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
    
    def get_option(self):
        return {}
    
    def getAdviseHeads(self,heads):
        """
        返回前端默认像是的字段名称，如：
        [name1,name2]
        """
        heads_names = [head['name'] for head in heads]
        return heads_names
    
    @request_cache
    def get_head_context(self):
        """
        有些时候，最先不需要返回rows，而只返回filters，head等，等待用户选择后，才返回rows
        
        {
            opMergeCount:3
        }
        """
        ops = self.get_operation()
        ops = evalue_container(ops)
        
        heads = self.get_heads()
        # 这样写，为了不影响这种写法: {fitWidth:True,**Mytab().get_head_context() }
        dc = {}
        if self.fitWidth:
            dc.update({
                'fitWidth':True
            })
        if self.allow_set_layout:
            request = get_request_cache()['request']
            dc.update({
                'advise_heads':self.getAdviseHeads(heads),
                'advise_heads_cookie_path':request.get_full_path()
            })
        return {
            'heads':heads,
            'rows': [], #self.get_rows(),
            'row_pages':{}, # self.pagenum.get_context(),
            'row_sort':self.row_sort.get_context(),
            'row_filters': self.getRowFilters() , #self.row_filter.get_context(),
            'search_args': self.search_args,
            'option':self.get_option(),
            #'search_tip':self.row_search.get_context(),
            'director_name': self.get_director_name(),#model_to_name(self.model),
            'ops' : ops, 
            'selectable': self.selectable,
            'event_slots':self.get_event_slots(),
            'autoLoad':self.autoLoad,
            **dc,
        }  
    
    def get_context(self):
        head_ctx = self.get_head_context()
        data_ctx = self.get_data_context()
        head_ctx.update(data_ctx)
        head_ctx.update({
            'row_sort': self.getRowSort()
        })
        return head_ctx
    
    def get_event_slots(self):
        return []
    
    def getRowFilters(self): 
        ls=[]
        search_head = self.row_search.get_context()
        row_filters = self.row_filter.get_context()
        # 合并search和rowfilter 为rowfilter
        if search_head:
            ls.append( search_head)
        if row_filters:
            #ls.extend(row_filters)
            # 把有默认值的filter排在前面
            f1 = []
            f2 = []
            for row in row_filters:
                if row.get('name') in self.search_args or '_start_'+row.get('name') in self.search_args or\
                   '_end_'+row.get('name') in self.search_args:
                    f1 .append(row)
                else:
                    f2.append(row)
            ls.extend(f1)
            ls.extend(f2)            
            
        return ls
    
    def getParents(self): 
        return []
    
    def get_data_context(self):
        rows =  self.get_rows()
        self.rows_count = len(rows)
        if self.only_simple_data():
            out_dc ={
                'rows':rows,
                'footer': self.footer,
                'parents': self.getParents(),
                'row_pages' : self.getRowPages(),
            }
            if not out_dc['footer']:
                out_dc.pop('footer')
            if not out_dc['parents']:
                out_dc.pop('parents')
            return out_dc
        else:
            table_layout = self.getTableLayout(rows)
            dc = {
                'rows': rows,
                'table_layout': table_layout,
                'row_pages' : self.getRowPages(), #self.pagenum.get_context(),  
                'search_args':self.search_args, 
                'footer': self.footer,
                'parents': self.getParents(),
             }
            return dc
    
    def getTableLayout(self, rows): 
        return {}
    
    def getRowPages(self): 
        return self.pagenum.get_context()
    
    def getRowSort(self):
        return self.row_sort.get_context()
    
    def permited_fields(self):
        ls = self.permit.readable_fields()
        
        if 'id' not in self.exclude and 'id' not in ls:
            ls.insert(0,'id')
        elif 'id' in self.exclude and 'id' in ls:
            ls.remove('id')
            
        if self.include != None:
            return [x for x in self.include if x in ls]
        if self.exclude:
            return [x for x in ls if x not in self.exclude]
        return ls
    
    def getExtraHead(self):
              
        if self.button_edit:
            model_form = director.get(self.get_edit_director_name())
            if model_form:
                form_obj = model_form(crt_user=self.crt_user)
                fields_ctx = form_obj.get_head_context()              
                return [ 
                    {'name':'_op',
                     'label':'操作',
                     'editor':'com-table-button-click',
                     'button_label':'详情',
                     'fields_ctx':fields_ctx,
                     'click_express':pop_edit_current_row(),                      }
                  ]
            
        return []
    
    @request_cache
    def get_heads(self):
        """
        return:[{"name": "name", "label": "\u59d3\u540d"}, {"sortable": true, "name": "age", "label": "\u5e74\u9f84"}]
        """
        if self.has_sequence:
            heads = [
                {'name': '_sequence', 'label': '序号', 'editor': 'com-table-sequence', 'inn_editor': 'com-table-sequence',}
            ]
        else:
            heads = []
        model_heads = self.get_model_heads()
        heads =  heads + model_heads
        if  self.include ==None:
            heads = [x for x in heads if x['name'] not in self.exclude]
        else:
            heads = [x for x in heads if x['name'] in self.include]
            
        heads += self.getExtraHead() 
        
        # 增加桥接
        for bridge in self.foreign_bridge:
            heads +=  bridge.getHeads()        
        
        for head in heads:
            if 'editor' not in head:
                head['editor'] = 'com-table-span'
                
        heads= self.make_pop_edit_field(heads)  
        heads = [self.dict_head(head) for head in heads]
        heads = self.fields_sort_heads(heads)  
        # 需要使用form.field才能提取到choices
        #form_fields = fields_for_model(self.model)
        #for head in model_heads:
            ##field = self.model._meta.get_field(head['name'])  
            #if 'options' in head:
                #continue
            #field =  form_fields.get(head['name'])
            #if hasattr(field, 'choices'):
                #catch = get_request_cache()
                #options_name = '%s_field_options'% ( model_to_name(self.model) + head['name'])
                #if not catch.get(options_name):
                    #catch[options_name]=[{'value':val,'label':str(lab)} for val,lab in field.choices]    
                #head['options']=catch.get(options_name)
                
        heads=evalue_container(heads)

            
        heads = sorted(heads,key=lambda head: head.get('order',0))
        
        # start: 实现 after_fields 排序
        after_fields_list =[]
        after_dict = {}
        for head in heads:
            if head.get('after_fields'):
                after_fields_list.extend(head.get('after_fields'))
                after_dict[head['name']]=[]
                for item in  head.get('after_fields'):
                    item_head = findone(heads, {'name':item})
                    if item_head:
                        after_dict[head['name']].append(item_head)
                
        
        lefts = [x for x in heads if x['name'] not in after_fields_list ]
        for k,v in after_dict.items():
            index = find_index(lefts,{'name':k})
            lefts[index:index] = v
        return lefts
                
        
        
        
        #heads_dict={}
        #for head in heads:
            #order_after = head.get('order_after')
            #if order_after:
                #if order_after not in heads_dict:
                    #heads_dict[order_after] =[]
                #heads_dict[order_after].append(head)
        
        #out_heads =[]
        #for head in list( heads):
            #if head.get('order_after'):
                #continue
            #out_heads.append(head)
            #if head['name'] in heads_dict:
                #out_heads.extend(heads_dict[head['name']])
        # end:
        #return out_heads
    
    def get_model_heads(self): 
        ls = self.permited_fields()   
        visible_fields = [x for x in ls if x not in self.hide_fields]
        heads = []
        model_name = model_to_name(self.model)
        for field in self.model._meta.get_fields():
            if isinstance(field,models.Field): # 可能是为了排除 related_object
                dc= {'name':field.name,'label': str(field.verbose_name) }  #_(str(field.verbose_name)) }  #  _(field.verbose_name)
                
                fieldName = model_name + '.' + field.name
                if fieldName in field_map:
                    mapper = field_map.get(fieldName)
                    mapper(name=field.name,model=self.model).dict_table_head(dc)
                elif field.__class__ in field_map:
                    mapper = field_map.get(field.__class__)
                    if hasattr(mapper,'dict_table_head'):
                        mapper(name=field.name,model=self.model,field=field).dict_table_head(dc)
                #elif isinstance(field,models.ForeignKey):
                    #dc['editor']='com-table-label-shower'            
                    
                heads.append(dc)

        heads=[x for x in heads if x.get('name') in visible_fields]
        #heads.sort(key=lambda x : heads.index(x.get('name')))
        return heads
    
    @request_cache
    def get_light_heads(self): 
        heads = self.get_model_heads()
        heads.extend(self.getExtraHead())
        heads = self.fields_sort_heads(heads)   
        return heads 
    
    def footer_by_dict(self, dc): 
        """
        2020/3/17 现在前端做了处理，footer直接传字典就可以解析了。这个函数应该无用了。
        
        由于elment-ui table只能接受数组作为footer，这里将 {'field':'sumvalue'} 形式的字典，转换为
        [sumvalue] 这样的数组，便于前端element table 的foot 显示。
        
        """
        heads= self.get_light_heads()
        footer = []
        for head in heads:
            if head.get('children'):
                continue
            footer.append(dc.get(head['name'], ''))
        return footer
    
    def make_pop_edit_field(self,heads):
        """
        确定弹出框 列
        """
        if self.pop_edit_field:
            for head in heads:
                if head['name']==self.pop_edit_field:
                    director_name = self.get_director_name()
                    #model_form = model_dc[self.model].get('fields')
                    model_form = director.get(self.get_edit_director_name())
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
                    #head['ops']=form_obj.get_operations()
                    #head['extra_mixins']=form_obj.extra_mixins
        if self.pop_edit_fields:
            model_form = director.get(self.get_edit_director_name())
            if model_form:
                form_obj = model_form(crt_user=self.crt_user)
                fields_ctx = form_obj.get_head_context()
                for head in heads:
                    if head['name'] in self.pop_edit_fields:
                        if head.get('editor'):
                            head['inn_editor'] = head['editor']
                        head['editor'] = 'com-table-click'
                        head['fields_ctx'] = fields_ctx
                        head['fields_ctx'].update({
                            #'after_save':'scope.vc.par_row.car_no =scope.row.car_no; scope.vc.par_row.has_washed=scope.row.has_washed ',
                            #'init_express':'cfg.show_load(),ex.director_call(scope.vc.ctx.director_name,{pk:scope.vc.par_row.pk}).then((res)=>{cfg.hide_load();ex.vueAssign(scope.row,res.row)})',
                           
                            #'mounted_express':'ex.vueAssign(scope.row,scope.vc.par_row)',
                            #'after_save':'ex.vueAssign( scope.vc.par_row,scope.row)',
                            'ops_loc':'bottom',
                            # 把初始化row放到 action里面去了 [1]
                            #'mounted_express':'ex.vueAssign(scope.row,ex.copy(scope.vc.par_row))',
                        })
                        head['action'] = ''' scope.head.fields_ctx.genVc=scope.vc;
                        scope.head.fields_ctx.title=scope.row._label;
                        scope.head.fields_ctx.par_row=scope.row;
                        scope.head.fields_ctx.row = ex.copy(scope.row); // [1] 如果不是编辑par_row ，可以修改这行
                        cfg.pop_vue_com("com-form-one",scope.head.fields_ctx,{maxmin: true})'''
                    
        return heads
    
    def dict_head(self,head):
        return head
    
    def fields_map_head(self,head):
        """
        fieldproc 处理
        [2018/6/22] 现在 field_proc 在 model_to_head 里面，这个函数可以没什么用了。
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
                    break
        return tmp_heads
    
    def before_query(self):
        pass
    
    def getCountQuery(self,query,before_innfilter_query):
        return getattr(self,'count_query',None)
        #return None
    
    def get_rows(self):
        """
        return: [{"name": "heyul0", "age": "32", "user": null, "pk": 1, "_class": "user_admin.BasicInfo", "id": 1}]
        """
        query=self.get_query()
      
        query = self.pagenum.get_query(query,countQuery = self.count_query)  
        out=[]
        #director_name = self.get_director_name()
        permit_fields =  self.permited_fields()
        #used_head_names= self.hide_fields +  [x['name'] for x in self.get_light_heads()] 
        
        #[去掉联查] 联查的字段不要走 sim_dict函数，否则会走forign_pro
        if self.exclude_export_related:
            normd_permit_fields = [x for x in permit_fields if x not in self.exclude_export_related]
        else:
            normd_permit_fields = permit_fields
            
        self.before_query()
        for inst in query:
            # 遇到一种情况，聚合时，这里的queryset返回的item是dict。所以下面做一个判断
            if isinstance(inst,models.Model):
                cus_dict = self.dict_row( inst)
                if self.only_simple_data():
                    dc = sim_dict(inst, include=normd_permit_fields,filt_attr=cus_dict,) # include_pk=False
                else:
                    dc= to_dict(inst, include=normd_permit_fields,filt_attr=cus_dict)
                    dc .update({
                        '_director_name':self.get_edit_director_name(),
                        'meta_org_dict':self.get_org_dict(dc,inst)
                        })
                #[去掉联查] 联查的字段不要走 sim_dict函数，否则会走forign_pro
                for name in  self.exclude_export_related:
                    dc[name] = getattr(inst,f'{name}_id',None)
                    dc[f'_{name}_label'] = getattr(inst,f'{name}_id','')
                # 再赋值一次，以免被默认dictfy替换掉了，例如 _x_label等值
                dc.update(cus_dict)
            else:
                dc = self.dict_row( inst)
                if not self.only_simple_data():
                    dc .update({
                       '_director_name':self.get_edit_director_name(),
                       'meta_org_dict':self.get_org_dict(dc,inst)
                       })
            out.append(dc)
            # 增加桥接
            for bridge in self.foreign_bridge:
                dc.update(  bridge.getRow(inst)  )   
                #if bridge.field_name in dc:
                    #del dc[bridge.field_name]
                #if f'_{bridge.field_name}_label' in dc:
                    #del dc[f'_{bridge.field_name}_label']
                #if f'_{bridge.field_name}_model' in dc:
                    #del dc[f'_{bridge.field_name}_model']                
        return out
    
    def get_model_field_name(self):
        fields =self.model._meta.get_fields()
        fields=[field for field in fields if isinstance(field,models.Field)]
        if self.include != None :
            fields=filter(lambda field:field.name in self.include,fields)
        if self.exclude != None:
            fields=filter(lambda field:field.name not in self.exclude,fields)
        return [x.name for x in fields]
            #model_path = instance._meta.app_label+'.'+instance._meta.model_name
    #fields=instance._meta.get_fields() # 如果用  instance._meta.fields 没有 manytomany (测试过) ,可能也没有 onetoone
    #fields=[field for field in fields if isinstance(field,models.Field)]
    #if include != None :
        #fields=filter(lambda field:field.name in include,fields)
    #if exclude != None:
        #fields=filter(lambda field:field.name not in exclude,fields)
        
    def get_org_dict(self,row,inst=None):
        org_row = make_mark_dict(row)
        return org_row
    
    def only_simple_data(self):
        return self.simple_dict or self.kw.get('_accept')=='json'
    
    
    @classmethod
    def get_edit_director_name(cls): 
        return cls.get_director_name() + '.edit'
    

    
    def dict_row(self,inst):
        """
        重写该函数，定制row输出字典
        """
        if isinstance(inst,dict):
            return inst
        else:
            return {}
    
    #def init_query(self):
        #return self.model.objects.all()
    
    def get_query(self):
        if self.nolimit:
            pass
        elif not self.crt_user.is_authenticated():
            raise  UnAuth401Exception('no permission to browse %s ,Please login first' % self.model._meta.model_name)
        elif not self.crt_user.is_superuser and not self.permit.readable_fields():
            raise PermissionDenied('user %s ,no permission to browse %s'% ( self.crt_user.username, self.model._meta.model_name))
        #query =  self.init_query()
        query = self.model.objects.all()
        
        # 优化速度
        if self.exclude:
            query = query.defer(*self.exclude)
        
        if getattr(self.model,'filterByUser',None):
            query = self.model.filterByUser(user=self.crt_user,query=query)
        before_innfilter_query = query
        query = self.inn_filter(query)
        #[count-] 有时单独计算count，效率很高。
        count_query = self.getCountQuery(query,before_innfilter_query=before_innfilter_query)
        if count_query != None:
            count_query= self.row_filter.get_query(count_query)
            count_query = self.row_search.get_query(count_query)
            self.count_query=count_query 
        # [-count]

        query=self.row_filter.get_query(query)
        query=self.row_search.get_query(query)
        
        query = self.statistics(query)
        query = self.row_sort.get_query(query)
        
        #[todo] 这里需要弄清楚原理
        #[todo_已经完成] 优化，是否select_related,select_related的field限定在输出的head中
        if not query._fields and self.export_related:  # 如果query._fields属性部位不为空，证明已经调用了.values() or .values_list()
            head_nams = [x['name'] for x in self.get_light_heads() if x['name'] not in self.exclude_export_related]
            for f in self.model._meta.get_fields():
                if f.name in head_nams and isinstance(f, (models.ForeignKey,models.OneToOneField)):
                    query = query.select_related(f.name)  
                if f.name in head_nams and isinstance(f,models.ManyToManyField):
                    query = query.prefetch_related(f.name)

        
        return query
    
    def statistics(self,query):
        """
        # 因为统计会破坏pk的存在，所以把排序放在统计函数里面
        现在 排序 完全放到 RowSort里面去了
        """
        return query
    
    
    def inn_filter(self,query):
        return query
    
    def get_operations(self):
        director_name = self.get_director_name()
        #model_form = model_dc[self.model].get('fields')
        #has_not_filter_or_search = ( self.filters ==RowFilter and self.search in [RowSearch] )
        
        refresh_action = {'name':'refresh',
                 'editor':'com-btn-el-button',
                 'label':'',
                 'title':'refresh',
                 #'class':'com-btn-refresh-btn',
                 'icon':'el-icon-refresh',
                 #'css':'.com-btn-refresh-btn{float:right}',
                 "utility":True,
                 #'type':'success',
                 'plain':True,
                  'show_express':'rt = !(scope.ps.vc.operationHeads.length == 1 && scope.ps.vc.filterHeads.length >=1) ',
                  # 在没有搜索栏的时候，再显示一个刷新按钮
                 'visible':  self.allow_refresh and self.filters ==RowFilter and self.search in [RowSearch], # , #
                 'action':'scope.ps.search()'}
        table_setting = {'editor':'com-btn-el-button',
             'name':'table_setting',
            'label':'',  # 
            'title':'设置列显示和排序',
            'utility':True,
            'plain':True,
            'icon':'el-icon-s-tools',
            'click_express':'''cfg.pop_vue_com("com-d-table-setting",{table_ps:scope.ps,title:"设置列的排序和显示(拖动可以调整顺序,勾选控制是否显示)"})
                           .then(()=>scope.ps.reloadAdviseInfo())''',
            'visible':self.allow_set_layout}
        fieldCls = director.get(director_name+'.edit')     
        if not fieldCls:
            return [
                table_setting,
                refresh_action
            ]
            
        fieldobj=fieldCls(crt_user=self.crt_user)
        fields_ctx = fieldobj.get_head_context()
        fields_ctx.update({
            'ops_loc':'bottom'
        })
        
        
        if self.check_cascade_delete:
            delete_js='''(async ()=>{
                     cfg.show_load();
                     var resp = await ex.director_get("d.delete_query_related",{rows:scope.ps.selected})
                     cfg.hide_load();
                     var confirm_delete = true;
                     if(resp.length>0){
                         confirm_delete = await cfg.pop_vue_com("com-pan-delete-query-message",{msg_list:resp,title:"删除关联确认"})
                     }
                     if(confirm_delete){
                        scope.ps.delete_selected()
                     }
                     
                 } )()
                 '''
        else:
            delete_js='''(async ()=>{
                    scope.ps.delete_selected()                     
                 } )()
                     '''
        
        return [
            table_setting,    
            refresh_action,
            
            {
                'name':'add_new',
                 #'editor':'com-op-btn',
                 #'icon': 'fa-plus',
                 #'class':'btn btn-primary btn-sm',
                 'editor':'com-btn',
                 'click_express':'scope.head.fields_ctx.genVc=scope.vc;scope.ps.add_new(scope.head)',
                 'icon':'el-icon-plus',
                 'type':'primary',
                 'label':_('创建'),
                 'pre_set':'', # 预先设置的字段,一般用于com-tab-table下的创建
                 'fields_ctx':fields_ctx,
                 'visible': self.permit.can_add() and self.allow_create,
                 },
                #{'name':'save_changed_rows','editor':'com-op-btn','label':'保存', 
                 #'class':'btn btn-info btn-sm',
                 #'show': 'scope.changed','hide':'!changed','icon':'fa-save', 'visible': self.permit.can_edit()},
                #{'name':'delete_selected',
                 #'editor':'com-op-btn',
                 #'label':'删除',
                 #'style': 'color:red',
                 #'icon': 'fa-times',
                 #'disabled':'!scope.ps.has_select', 
                 #'visible': self.permit.can_del(),},
                {'name':'delete_selected',
                 'editor':'com-btn',
                 'label':_('删除'),
                 'click_express':delete_js ,
                 
                 #'''
                   #cfg.show_load();ex.director_call("d.delete_query_related",{rows:scope.ps.selected}).then((resp)=>{
                     #cfg.hide_load();
                     #if(resp.length>0){
                         #cfg.pop_vue_com("com-pan-delete-query-message",{msg_list:resp,genStore:scope.ps,title:"删除关联确认"})
                     #}else{
                        #scope.ps.delete_selected()
                     #}
                    
                 #});
                 #'''
                 
                 # if(scope.ps.check_selected(scope.head)){scope.ps.delete_selected()}
                 #'style': 'color:red',
                 #'icon': 'fa-times',
                 'type':'danger',
                 #'plain':True,
                 'icon':'el-icon-delete',
                 'row_match':'many_row',
                 'disabled':'!scope.ps.has_select', 
                 'visible': self.allow_delete  and self.permit.can_del() },
               
                ]     
        
    
    def get_operation(self):
        '兼容老的调用,'
        return self.get_operations()
    
    def getExcelRows(self):
        return self.get_rows()
    
    def getExcelHead(self):
        return self.get_heads()
    
    def get_excel(self): 
        from openpyxl import Workbook
        
        #self.search_args['_perpage'] = 5000
        #ctx = self.get_context()
        self.is_export_excel = True
       

        heads = self.getExcelHead() #ctx['heads']
        rows =  self.getExcelRows() #ctx['rows']
        out_rows = []
        excel_row = []
        # 第一行是 头
        for head in heads:
            if head.get('children'):
                continue
            excel_row.append(head['label'])
            if 'options' in head and head['options']:
                head['options_dict'] = {}
                for opt in head['options']:
                    head['options_dict'][opt['value']] = opt['label'] 
        out_rows.append(excel_row)
        
        # 这里开始写数据
        for row in rows:
            excel_row = []
            for head in heads:
                if head.get('children'):
                    continue
                label = '_%s_label' % head['name']
                if label in row:
                    excel_row.append( row.get(label) )
                elif 'options_dict' in head:
                    value = row.get(head['name'])
                    find_label = head['options_dict'].get(value, '')
                    excel_row.append( find_label )
                else:
                    excel_row.append( row.get(head['name']) )
            out_rows.append(excel_row)
        
        wb = Workbook()
        ws = wb.active       
        for row in out_rows:
            #ws.append(row)
            # 有可能是models.py lazy翻译的
            ws.append([str_lazy_label(x)  for x in row ])        
        self.after_excel(wb,ws,out_rows)
        return wb
    def after_excel(self,wb,ws,out_rows):
        "用户设置ws的单元格格式等"
        pass

class RawTable(ModelTable):
    '''
    1. 重写 get_sql
    
    '''
    def get_sql(self):
        pass
    
    def get_rows(self):
        self.params = []
        sql = self.get_sql()
        self.bucket=[]
        if sql:
            with connections[self.model.objects.db].cursor() as cursor:
                if isinstance(sql,list):
                    for item in sql:
                        cursor.execute(item.get('sql'),item.get('params',[]))
                        self.bucket.append( self.get_result(cursor) )
                else:
                    cursor.execute( sql ,self.params,)
                    try:
                        self.bucket.append( self.get_result(cursor) )
                    except ProgrammingError as e:
                        pass
                    while  cursor.nextset():
                        try:
                            self.bucket.append( self.get_result(cursor) )
                        except ProgrammingError as e:
                            pass
                        
            self.pagenum.count = self.bucket[1][0]['count']
            if len(self.bucket)>2:
                self.footer = self.bucket[2][0]
                self.footer['_label']='合计'
            out_rows = []
            for row in self.bucket[0]:
                row_dc = {k.lower():v for k,v in row.items()}
                row_dc.update({
                    '_director_name':self.get_edit_director_name(),
                    **self.dict_row(row_dc)
                })
                
                out_rows.append(row_dc)
            return out_rows
  
    def dict_row(self, row_dc):
        return {}
    
    def get_result(self,cursor):
        rows =[]
        for row in cursor:
            dc = {}
            for index, head in enumerate(cursor.description):
                dc[head[0]] = row[index]
            rows.append(dc)
        return rows
    
    def get_where(self):
        self.where_list =[]
        self.row_search.inject_sql(self.where_list,self.params)
        ss = ' AND '.join(self.where_list)
        if ss:
            return 'WHERE %s'%ss
        else:
            return ss
    
    def get_sort(self):
        search_args = self.kw.get('search_args')
        sort_str = search_args.get('_sort') or self.row_sort.general_sort

        if sort_str.startswith('-'):
            order_by = ' ORDER BY %s DESC '%sort_str[1:] 
        else:
            order_by = ' ORDER BY %s'% sort_str
        return  order_by
   
    def inject_sql(self,where_list,params):
        for proc_cls,name in zip(self.get_proc_list() ,self.valid_name):
            condition = proc_cls().filter_inject_sql(name ,self.filter_args )
            if condition:
                where_list.append(condition)
        
        
    #def get_query(self):
        #self.where_list =[]
        #self.params =[]
        #self.order_by=''
        
        #self.inject_sql()
        ##self.row_filter.inject_sql(self.where_list,self.params)
        ##self.row_search.inject_sql(self.where_list,self.params)
        ##if self.where_list:
            ##self.sql += ' WHERE ' + ' AND '.join(self.where_list)
        #self.query = self.model.objects.raw(self.sql+self.order_by,self.params)
        #self.query.count = lambda : self.update_count()
        #self.statistics(self.query)
        
        #return self.query
    
        #rows = []
        #for row in query:
            #dc = self.dict_row(row)
            #rows.append(to_dict(row,filt_attr = dc))
        #return rows
    
    #def getRowPages(self): 
        
        #return {'crt_page':1, #self.pageNumber,
               #'total':self.count,
               #'perpage': 20#self.perPage
               #}
    
    #def update_count(self):
        #with connections[self.query.db].cursor() as cursor:
            #cursor.execute( 'SELECT COUNT(*) FROM (' + self.sql + ') bba' ,self.params)
            #set0 = cursor.fetchall()
            #return set0[0][0]
    
    #def get_foot_sql(self):
        #self.foot_field=[]
        #return ''
    
    #def statistics(self, query):
        #sql = self.get_foot_sql()
        #if sql:
            #with connections[self.query.db].cursor() as cursor:
                #cursor.execute( sql ,self.params)
                #for row in cursor:
                    #dc = {}
                    #for index, head in enumerate(cursor.description):
                        #dc[head[0]] = row[index]
                    #dc['_label']='合计'
                #self.footer=dc
                
        
    
            


class PlainTable(ModelTable):
    def __init__(self,page=1,row_sort=[],row_filter={},row_search= '',crt_user=None,perpage=None,**kw):
        """
        kw['search_args']只是一个记录，在获取到rows时，一并返回前端页面，便于显示。
        而真正的查询参数已经被路由到各个查询组件中，具体参见 cls.parse_request / gen_from_search_args 函数
        如果需要设置查询的默认参数，需要到 cls.clean_search_args中去设置
        
        """
        self.search_args = kw.get('search_args', {})
        
        self.kw=kw
        self.crt_user=crt_user or get_request_cache()['request'].user
        
        #allowed_names = []
        #self.row_sort=self.sort(row_sort,crt_user,allowed_names,kw)
        #self.row_filter=self.filters(row_filter, crt_user, allowed_names,kw) 
        #self.row_search = self.search( row_search,crt_user,allowed_names,kw)
        
        self.page= int( page or 1 )
        self.perpage= int( perpage or 20 )
        self.footer = {}
        self.custom_permit()
    
    def custom_permit(self):
        pass
    
    def get_head_context(self):
        """
        有些时候，最先不需要返回rows，而只返回filters，head等，等待用户选择后，才返回rows
        """
        ops = self.get_operations()
        ops = evalue_container(ops)

        return {
            'fitWidth':self.fitWidth,
            'heads':self.get_heads(),
            'rows': [], #self.get_rows(),
            'row_pages':{}, # self.pagenum.get_context(),
            'row_sort':self.getRowSort(),
            'row_filters': self.getRowFilters() , #self.row_filter.get_context(),
            'search_args': {},
            #'search_tip':self.row_search.get_context(),
            'director_name': self.get_director_name(),#model_to_name(self.model),
            'ops' : ops,
            'selectable': self.selectable,
            'event_slots':self.get_event_slots()
        }  
    
    #def get_data_context(self):
        #return {
            #'rows': rows,
            #'row_pages' : self.getRowPages(),
            #'row_sort': self.getRowSort(),#row_sort,
            #'row_filters':  self.getRowFilters(), #ls,
        #}
    
    def get_context(self):
        out_dict = self.get_head_context()
        out_dict.update(
            self.get_data_context()
        )
        return out_dict
        
        #return {
            #'heads':heads,
            #'rows': rows,
            #'row_pages' : self.getRowPages(),
            #'row_sort': self.getRowSort(),#row_sort,
            #'row_filters':  self.getRowFilters(), #ls,
            ##'search_tip':self.row_search.get_context(),
            #'director_name':director_name,
            #'ops' : ops,
            #'search_args':self.search_args, 
            #'parents': self.getParents(),
            #'footer': self.footer,
            #'selectable': self.selectable,
            #'event_slots':self.get_event_slots()
        #}    
    def get_operations(self):
        return []
    
    def getRowSort(self): 
        return {
            'sortable': [],
        }
    
    def getRowFilters(self): 
        return []
    
    def getRowPages(self): 
        per_page = math.ceil(self.rows_count /100) *100 
        return {
            'total':self.rows_count,
            'perPage':per_page,
            'options':[per_page],
            'crt_page':1,
        }  
        