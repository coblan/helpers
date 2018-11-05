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
from django.core.exceptions import FieldDoesNotExist
from helpers.director.middleware.request_cache import get_request_cache
from helpers.director.model_func.field_proc import BaseFieldProc
from helpers.func.collection.container import evalue_container

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
        
        # 需要研究下，为什么有时 len(query) != query.count()  ，例如 jb.maindb.ticket_admin.TicketparlayTable
        #self.count =  len(query) #query.count()
        
        #crt_page=max(1,int( self.pageNumber))
        #start = (crt_page -1)*self.perPage
        #end = min(crt_page*self.perPage, self.count)
        #return query[start:end]
        self.pagenator = Paginator(query,self.perPage)
        self.pageNumber = min(self.pagenator.num_pages,abs(int( self.pageNumber)))
        self.count = self.pagenator.count
        return self.pagenator.page(self.pageNumber)
 
        
        
    
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
    def __init__(self,pageNumber=1,kw={}):
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
    
     range_fields=[{'name':'create_time','type':'date'}]
    """
    names=[]
    range_fields=[]
    model=''
    def __init__(self,dc,user,allowed_names,kw={}):
        # 为了让前端不显示
        self.model_allowed_names =  allowed_names
        
        # [todo] 应该把属于 model的字段，利用allowd_names 过滤掉
        self.names = self.names + self.range_fields #+ [x.get('name') for x in self.range_fields]
        self.valid_name= self.names  #[x for x in self.names if x in allowed_names]
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
        self.kw = kw
    
    def get_proc_list(self):
        ls=[]
        has_model = getattr(self, 'model')
        if has_model:
            field_names = [f.name for f in self.model._meta.get_fields()]
        else:
            field_names = []
        for name in self.valid_name:
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
        dc = {x['name']: x  for x in extraHead }
        valid_model_names = [x for x in self.names if x in self.model_allowed_names]
        send_to_front_names = valid_model_names + [x['name'] for x in extraHead]
        for proc_cls,name in zip(self.get_proc_list() ,self.valid_name):
            if name in dc:
                # 为了性能考虑，如果有head了，就不进行自动生成head了，并且排除掉那些不在model里面的字段
                #normal_heads.append(dc[name])
                continue
            
            if name in self.range_fields:
                filter_head = proc_cls().filter_get_range_head(name,self.model)
                normal_heads.append(filter_head)
  
            else:
                filter_head = proc_cls().filter_get_head(name,self.model)
                normal_heads.append(filter_head)
        
        out_list = extraHead
        out_list.extend(normal_heads)
        out_list = [self.dict_head(head) for head in out_list]
        out_list = [x for x in out_list if x['name'] in send_to_front_names]
        out_list = sorted(out_list, key= lambda x: send_to_front_names.index(x['name']))
        return out_list
    
    def clean_query(self, query): 
        return query
    
    def get_query(self,query):
        self.query=query
        dc = {}
        for proc_cls,name in zip(self.get_proc_list() ,self.valid_name):
            value =  self.filter_args.get(name, None)
            if value != None:
                dc[name] = proc_cls().filter_clean_filter_arg(value ) 
        self.filter_args.update(dc)
        arg_dc = {k: v for k, v in self.filter_args.items() if v != None}
        
        query=query.filter(**arg_dc)
        query = self.clean_query(query)
        return query    
    
class RowSort(object):
    """
    row_sort: 'name1,-name2'
    """
    names=[]
    chinese_words=[]
    def __init__(self,row_sort=[],user=None,allowed_names=[],kw={}):
        #final_allowd_names = allowed_names + self.extra_allowd_names
        #self.valid_name=[x for x in self.names if x in final_allowd_names]
        self.valid_name=[x for x in self.names]
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
                    query= query.order_by(name, '-pk')
        else:
            query = query.order_by('-pk')

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
        """
        kw['search_args']只是一个记录，在获取到rows时，一并返回前端页面，便于显示。
        而真正的查询参数已经被路由到各个查询组件中，具体参见 cls.parse_request / gen_from_search_args 函数
        如果需要设置查询的默认参数，需要到 cls.clean_search_args中去设置
        
        """
        self.search_args = kw.get('search_args', {})
        
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
        self.footer = []
        
    
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
        director_name =self.get_director_name()
        heads = self.get_heads()
        rows = self.get_rows()
        row_sort = self.row_sort.get_context()
        model_name = model_to_name(self.model)
        ops = self.get_operation()
        ops = evalue_container(ops)
        return {
            'heads':heads,
            'rows': rows,
            'row_pages' : self.getRowPages(),
            'row_sort':row_sort,
            'row_filters':  self.getRowFilters(), #ls,
            #'search_tip':self.row_search.get_context(),
            'director_name':director_name,
            'model_name':model_name,
            'ops' : ops,
            'search_args':self.search_args, 
            'parents': self.getParents(),
            'footer': self.footer,
        }
    
    def getRowFilters(self): 
        ls=[]
        search_head = self.row_search.get_context()
        row_filters = self.row_filter.get_context()
        # 合并search和rowfilter 为rowfilter
        if search_head:
            ls.append( search_head)
        if row_filters:
            ls.extend(row_filters)
        return ls
    
    def get_head_context(self):
        """
        有些时候，最先不需要返回rows，而只返回filters，head等，等待用户选择后，才返回rows
        """
        #ls=[]
        #search_head = self.row_search.get_context()
        #row_filters = self.row_filter.get_context()
        ## 合并search和rowfilter 为rowfilter
        #if search_head:
            #ls.append( search_head)
        #if row_filters:
            #ls.extend(row_filters)
        ops = self.get_operation()
        ops = evalue_container(ops)
        return {
            'heads':self.get_heads(),
            'rows': [], #self.get_rows(),
            'row_pages':{}, # self.pagenum.get_context(),
            'row_sort':self.row_sort.get_context(),
            'row_filters': self.getRowFilters() , #self.row_filter.get_context(),
            'search_args': {},
            #'search_tip':self.row_search.get_context(),
            'director_name': self.get_director_name(),#model_to_name(self.model),
            'ops' : ops
        }        
    
    def getParents(self): 
        return []
    
    def get_data_context(self):
        rows =  self.get_rows()
        table_layout = self.getTableLayout(rows)
        return {
            'rows': rows,
            'table_layout': table_layout,
            'row_pages' : self.getRowPages(), #self.pagenum.get_context(),  
            'search_args':self.search_args, 
            'footer': self.footer,
            'parents': self.getParents(),
        }
    
    def getTableLayout(self, rows): 
        return {}
    
    def getRowPages(self): 
        return self.pagenum.get_context()
    
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
        model_heads = self.get_model_heads()
        heads = model_heads + self.getExtraHead() 
        heads = self.fields_sort_heads(heads)   
        heads= self.make_pop_edit_field(heads)  
        heads = [self.dict_head(head) for head in heads]
        
        for head in model_heads:
            field = self.model._meta.get_field(head['name'])            
            if hasattr(field, 'choices') and 'options' not in head :
                catch = get_request_cache()
                options_name = '%s_field_options'% ( model_to_name(self.model) + head['name'])
                if not catch.get(options_name):
                    catch[options_name]=[{'value':val,'label':str(lab)} for val,lab in field.choices]    
                head['options']=catch.get(options_name)
        return heads
    
    def get_model_heads(self): 
        ls = self.permited_fields()   
        ls = [x for x in ls if x not in self.hide_fields]
        heads = model_to_head(self.model,include=ls)
        return heads
    
    def get_light_heads(self): 
        heads = self.get_model_heads()
        heads.extend(self.getExtraHead())
        heads = self.fields_sort_heads(heads)   
        return heads 
    
    def footer_by_dict(self, dc): 
        """
        将 {'field':'sumvalue'} 形式的字典，转换为
        [sumvalue] 这样的数组，便于前端element table 的foot 显示。
        
        """
        heads= self.get_light_heads()
        footer = []
        for head in heads:
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
        permit_fields =  self.permited_fields()
        #used_head_names= self.hide_fields +  [x['name'] for x in self.get_light_heads()] 
        
        for inst in query:
            # 遇到一种情况，聚合时，这里的queryset返回的item是dict。所以下面做一个判断
            if isinstance(inst,models.Model):
                dc= to_dict(inst, include=permit_fields,filt_attr=self.dict_row( inst))
            else:
                dc = inst
            dc['_director_name'] = self.get_edit_director_name()
            out.append(dc)
        return out
    
    @classmethod
    def get_edit_director_name(cls): 
        return cls.get_director_name() + '.edit'
    

    
    def dict_row(self,inst):
        """
        重写该函数，定制row输出字典
        """
        return {}
    
    def get_query(self):
        if not self.crt_user.is_authenticated:
            raise PermissionDenied('no permission to browse %s ,Please login first' % self.model._meta.model_name)
        elif not self.crt_user.is_superuser and not self.permit.readable_fields():
            raise PermissionDenied('user %s ,no permission to browse %s'% ( self.crt_user.username, self.model._meta.model_name))
        query =  self.model.objects.all()
        
        # 优化速度
        if self.exclude:
            query = query.defer(*self.exclude)
        
        query = self.inn_filter(query)
        query=self.row_filter.get_query(query)
    
        query=self.row_search.get_query(query)
        query = self.statistics(query)
        query = self.row_sort.get_query(query)
        
        head_nams = [x['name'] for x in self.get_light_heads()]
        
        #[todo] 这里需要弄清楚原理
        #[todo] 优化，是否select_related,select_related的field限定在输出的head中
        if not query._fields:  # 如果这个属性部位空，证明已经调用了.values() or .values_list()
            for f in self.model._meta.get_fields():
                if f.name in head_nams and isinstance(f, models.ForeignKey):
                    query = query.select_related(f.name)        

        query = self.pagenum.get_query(query)  
        return query
    
    def statistics(self,query):
        """
        # 因为统计会破坏pk的存在，所以把排序放在统计函数里面
        现在 排序 完全放到 RowSort里面去了
        """
        return query
    
    
    def inn_filter(self,query):
        return query
    
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
                 'visible': self.permit.can_add(),
                 },
                {'name':'save_changed_rows','editor':'com-op-btn','label':'保存','hide':'!changed','icon':'fa-save', 'visible': self.permit.can_edit()},
                {'name':'delete','editor':'com-op-btn','label':'删除','style': 'color:red','icon': 'fa-times','disabled':'!has_select', 'visible': self.permit.can_del(),},
                ]      
    
    def get_excel(self): 
        from openpyxl import Workbook
        
        #self.search_args['_perpage'] = 5000
        ctx = self.get_context()
        heads = ctx['heads']
        rows = ctx['rows']
        out_rows = []
        
        excel_row = []
        for head in heads:
            excel_row.append(head['label'])
            if 'options' in head and head['options']:
                head['options_dict'] = {}
                for opt in head['options']:
                    head['options_dict'][opt['value']] = opt['label']
        out_rows.append(excel_row)
        
        for row in rows:
            excel_row = []
            for head in heads:
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
            ws.append(row)        
        
        return wb

class PlainTable(ModelTable):
    def __init__(self,_page=1,row_sort=[],row_filter={},row_search= '',crt_user=None,perpage=None,**kw):
        """
        kw['search_args']只是一个记录，在获取到rows时，一并返回前端页面，便于显示。
        而真正的查询参数已经被路由到各个查询组件中，具体参见 cls.parse_request / gen_from_search_args 函数
        如果需要设置查询的默认参数，需要到 cls.clean_search_args中去设置
        
        """
        self.search_args = kw.get('search_args', {})
        
        self.kw=kw
        self.crt_user=crt_user 
        self.page=_page
        self.footer = []
    
    def get_head_context(self):
        """
        有些时候，最先不需要返回rows，而只返回filters，head等，等待用户选择后，才返回rows
        """
        ops = self.get_operation()
        ops = evalue_container(ops)
        return {
            'heads':self.get_heads(),
            'rows': [], #self.get_rows(),
            'row_pages':{}, # self.pagenum.get_context(),
            'row_sort':self.getRowSort(),
            'row_filters': self.getRowFilters() , #self.row_filter.get_context(),
            'search_args': {},
            #'search_tip':self.row_search.get_context(),
            'director_name': self.get_director_name(),#model_to_name(self.model),
            'ops' : ops
        }  
    
    def getRowSort(self): 
        return {
            'sortable': [],
        }
    
    def getRowFilters(self): 
        return {}
    
    def getRowPages(self): 
        return {}  
        