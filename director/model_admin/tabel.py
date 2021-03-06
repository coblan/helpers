# encoding:utf-8

from __future__ import unicode_literals

#from core.db_tools import to_dict,model_to_head,model_stringfy
import json
from django.db.models import Q,fields
from django.core.exceptions import PermissionDenied
from permit import ModelPermit
from ..db_tools import model_to_name,to_dict,model_to_head,model_to_name
from django.db import models
import pinyin
from django.conf import settings
#from forms import MobilePageForm


from django.core.paginator import Paginator


class PageNum(object):
    perPage=20
    def __init__(self,pageNumber=1,kw={}):
        self.pageNumber = int(pageNumber)
    
    def get_query(self,query):
        self.pagenator = Paginator(query,self.perPage)
        self.query = query  
        page_num=min(self.pagenator.num_pages,abs(int( self.pageNumber)))
        return self.pagenator.page(page_num)
    
    def get_context(self):
        """
        rt: {'options':[1,2,3,4,...,100],
             'crt_page':2
            }
        """
        choice_len = len(self.pagenator.page_range)
        k=3
        a=-1
        while a < 1:
            a=self.pageNumber-k
            k-=1
        page_nums = range(a,min(choice_len,self.pageNumber+(5-k))+1)
        if page_nums[0] != 1:
            page_nums=[1,'...']+ page_nums
        if page_nums[-1] != choice_len:
            page_nums = page_nums +['...',choice_len]
        for i in range(len(page_nums)):
            num = page_nums[i]
        page_nums=[str(x) for x in page_nums]
        return {'options':page_nums,'crt_page':self.pageNumber}    

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
                ls.append(self.model._meta.get_field(name).verbose_name)
            return ','.join(ls)
        else:
            return None
    
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
        self.names = self.names + [x.get('name') for x in self.range_fields]
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
        for k in [x.get('name') for x in self.range_fields]:
            if kw.get('_start_%s'%k):
                start=kw.get('_start_%s'%k)
                self.filter_args['%s__gte'%k]=start
            if kw.get('_end_%s'%k):
                end=kw.get('_end_%s'%k)
                self.filter_args['%s__lte'%k]=end            
    
    def get_context(self):
        ls=[]
        for name in self.valid_name:
            f = self.model._meta.get_field(name)
            mt = [x for x in self.range_fields if x.get('name')==name]
            if mt:
                ls.append({'name':name,'label':f.verbose_name,'type':mt[0].get('type')})
            elif isinstance(f,fields.BooleanField):
                ls.append({'name':name,'label':f.verbose_name,'options':[
                {'value':'1','label':'Yes'},
                {'value':"0",'label':'No'}]})
            else:
                ls.append({'name':name,'label':f.verbose_name,'options':self.get_options(name)})
        return ls
      
    def get_query(self,query):
        self.query=query
        query=query.filter(**self.filter_args)
        return query    
    
    def get_options(self,name):
        this_field= self.model._meta.get_field(name)
        if this_field.choices:
            return [{'value':x[0],'label':x[1]} for x in this_field.choices]
        elif isinstance(this_field,models.ForeignKey):
            ls=this_field.get_choices()
            ls=ls[1:]
            out= [{'value':x[0],'label':x[1]} for x in ls]
            #out= self.sort_option(out) # 用pinyin排序 sorted(out,key=lambda x:x['label'].encode('gbk'))  # 尼玛，用GBK才能对常用的中国字进行拼音排序
                                                                   # 不常用的字，以及unicode都是按照笔画排序的
            return out
        elif not hasattr(self,'query'):
            return []
        else:
            ls = list(set(self.query.values_list(name,flat=True)))
            #ls.sort()
            out=[{'value':x,'label':unicode(x)} for x in ls]
            #out= self.sort_option(out) # 用pinyin排序 sorted(out,key=lambda x:x['label'].encode('gbk'))  
            return out   
    
    # def sort_option(self,option):
        # index=0
        # for opt in option:
            # if opt['value']:
                # break
            # else:
                # index+=1
        # option[index:]=sorted(option[index:],key=lambda x:pinyin.get_initial(x['label']))
        # return option
    
    
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


def chinese_order(query,norm_name,direction=''):
    """
    @norm_name: 张三
    @direction: - 负号
    """
    engine= settings.DATABASES.get(query.db)['ENGINE'] 
    if engine == 'django.contrib.gis.db.backends.postgis':
        # postgresql
        query= query.extra(select={'converted_%s'%norm_name: "convert_to(%s,'GBK')"%norm_name},order_by=['%sconverted_%s'%(direction,norm_name)])
    else:
        # mysql 按照拼音排序
        query= query.extra(select={'converted_%s'%norm_name: 'CONVERT(%s USING gbk)'%norm_name},order_by=['%sconverted_%s'%(direction,norm_name)])  
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
    pagenator=PageNum
    def __init__(self,page=1,row_sort=[],row_filter={},row_search={},crt_user=None,**kw):
        self.kw=kw
        self.crt_user=crt_user 
        self.page=page
        
        self.custom_permit()
        allowed_names=self.permited_fields()
        
        self.row_sort=self.sort(row_sort,crt_user,allowed_names,kw)
        self.row_filter=self.filters(row_filter, crt_user, allowed_names,kw) 
        self.row_search = self.search( row_search,crt_user,allowed_names,kw)
        if not self.row_filter.model:
            self.row_filter.model=self.model
        if not self.row_search.model:
            self.row_search.model=self.model
        self.pagenum = self.pagenator(pageNumber=self.page)
        
        
        
    
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
        page = kw.pop('_page','1')
        row_sort = kw.pop('_sort','').split(',')
        row_sort=filter(lambda x: x!='',row_sort)
        q=kw.pop('_q',None)
        row_filter={}
        for k in cls.filters.names:
            arg = kw.pop(k,None)
            if arg:
                row_filter[k]=arg
        return cls(page,row_sort,row_filter,q,request.user,**kw)    
        
    def get_context(self):
        return {
            'heads':self.get_heads(),
            'rows': self.get_rows(),
            'row_pages' : self.pagenum.get_context(),
            'row_sort':self.row_sort.get_context(),
            'row_filters':self.row_filter.get_context(),
            'search_tip':self.row_search.get_context(),
            'model':model_to_name(self.model),
        }
    
    def get_head_context(self):
        """
        有些时候，最先不需要返回rows，而只返回filters，head等，等待用户选择后，才返回rows
        """
        return {
            'heads':self.get_heads(),
            'rows': [], #self.get_rows(),
            'row_pages':{}, # self.pagenum.get_context(),
            'row_sort':self.row_sort.get_context(),
            'row_filters':self.row_filter.get_context(),
            'search_tip':self.row_search.get_context(),
            'model':model_to_name(self.model),
        }        
    
    def get_data_context(self):
        return {
            'rows': self.get_rows(),
            'row_pages' : self.pagenum.get_context(),            
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
    
    def get_heads(self):
        """
        return:[{"name": "name", "label": "\u59d3\u540d"}, {"sortable": true, "name": "age", "label": "\u5e74\u9f84"}]
        """
        ls = self.permited_fields()   
        heads = model_to_head(self.model,include=ls)
        heads = [self.dict_head(head) for head in heads]
        #for head in heads:
            #if head.get('name') in self.sortable:
                #head['sortable'] = True 
        return heads
    
    def get_rows(self):
        """
        return: [{"name": "heyul0", "age": "32", "user": null, "pk": 1, "_class": "user_admin.BasicInfo", "id": 1}]
        """
        query=self.get_query()
        out=[]
        for inst in query:

            dc= to_dict(inst, include=self.permited_fields(),filt_attr=self.dict_row( inst))
            out.append(dc)
        return out
    
    def dict_head(self,head):
        return head
    
    def dict_row(self,inst):
        """
        重写该函数，定制row输出字典
        """
        return {}
    
    def get_query(self):
        query = self.inn_filter(self.model.objects.all())
        query=self.row_filter.get_query(query)
    
        query=self.row_search.get_query(query)
        query = self.row_sort.get_query(query)
        query = self.pagenum.get_query(query)  
        return query
    #def page_filter(self,query):
        #self.pagenum = PageNum(query,perPage=self.perPage, pageNumber=self.page)
        #return self.pagenum.get_query()
    
    def inn_filter(self,query):
        if not self.crt_user.is_superuser and not self.permit.readable_fields():
            raise PermissionDenied,'no permission to browse %s'%self.model._meta.model_name
        else:
            return query.order_by('-id')
    
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
  