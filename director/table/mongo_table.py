from .table import PlainTable
from helpers.func.mongo import tm2mongo,mongo2tm
import datetime
from django.utils import timezone
from helpers.func.dict_list import sort_by_name,find_one

class MongoTable(PlainTable):

    model = None
    model_fields=[]
    fields=[]
    
    range_filter =[]
    value_filter = []
    sort_names =[]
    
    def __init__(self, *arg,**kws):
        super().__init__(*arg,**kws)
        self.filter_args = {}
        for name in self.range_filter:
            if self.search_args.get('_start_%s'%name):
                self.filter_args[name] = {'$gte' : tm2mongo( timezone.datetime.strptime( self.search_args.get('_start_%s'%name),'%Y-%m-%d %H:%M:%S' ) ) }
            if self.search_args.get('_end_%s'%name):
                query = {'$lte' : tm2mongo( timezone.datetime.strptime( self.search_args.get('_end_%s'%name),'%Y-%m-%d %H:%M:%S' ) )}
                if name not in  self.filter_args:
                    self.filter_args[name] = query
                else:
                    self.filter_args['EventDateTime'].update(query)
        for name in self.value_filter:
            if self.search_args.get(name):
                self._filter_value(name, self.search_args.get(name))
        
        if self.search_args.get('_qf') and  self.search_args.get('_q') !='':
            if self.search_args.get('_qf') in self.value_filter:
                self._filter_value(self.search_args.get('_qf') , self.search_args.get('_q'))
                
    def _filter_value(self,name,value):
        dtype = find_one(self.model_fields, {'name':name }).get('fieldtype')
        try:
            self.filter_args[ name ] = dtype( value )
        except ValueError as e:
            raise UserWarning('查询参数:%s 值为%s 不能正确转换为%s'%(name,value,dtype.__name__))
    
    def get_heads(self):
        heads = [{'name':x.get('name'),'label':x.get('label')} for x in self.model_fields if x.get('name') in self.fields]
        heads = sort_by_name(heads, self.fields,keep=False)
        heads=[self.dict_head(head) for head in heads]
        return heads
        
    def get_rows(self):
        start_index = ( self.page -1 ) * self.perpage
        rows =[]
        #'Event'
    
        #for item in spiderman['Ticket'].find(self.filter_args).sort( [('EventDateTime',1)]).skip(start_index).limit(self.perpage):
        
        for item in self.model.find(self.filter_args).sort( [('_id',-1)]).skip(start_index).limit(self.perpage):
            dc = {
                'pk':item.get('_id')
            }
            for key,value in item.items():
                if key == '_id':
                    dc['pk'] = str(value)
                elif isinstance(value,datetime.datetime):
                    dc[key] = mongo2tm(value)
                else:
                    dc[key] = value
                
            rows.append(dc)
            
        return rows
    
    def getRowPages(self):
        return {
            'crt_page':self.page,
            'total':self.model.find(self.filter_args).count(),
            'perpage':self.perpage,
        }