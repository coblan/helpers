from .table import ModelTable, PageNum

class SimTable(ModelTable):
    """
    一般用于，与model不相关的table
    """
    def __init__(self, _page=1, row_sort=[], row_filter={}, row_search='', crt_user=None, perpage=None, **kw): 
        self.search_args = kw.get('search_args')
        
        self.kw=kw
        self.crt_user=crt_user 
        self.page=_page
        
        #self.custom_permit()
        allowed_names= []  #self.permited_fields()
        
        self.row_sort=self.sort(row_sort,crt_user,allowed_names,kw)
        self.row_filter=self.filters(row_filter, crt_user, allowed_names,kw) 
        self.row_search = self.search( row_search,crt_user,allowed_names,kw)
        #if not self.row_filter.model:
            #self.row_filter.model=self.model
        #if not self.row_search.model:
            #self.row_search.model=self.model
        self.pagenum = self.pagenator(pageNumber=self.page,perpage=perpage)
    
    #def get_head_context(self): 
        #ls=[]
        #search_head = self.row_search.get_context()
        #row_filters = self.row_filter.get_context()
        ## 合并search和rowfilter 为rowfilter
        #if search_head:
            #ls.append( search_head)
        #if row_filters:
            #ls.extend(row_filters)
        #return {
            #'heads':self.get_heads(),
            #'rows': [], #self.get_rows(),
            #'row_pages':{}, # self.pagenum.get_context(),
            #'row_sort':self.row_sort.get_context(),
            #'row_filters': ls , 
            ##'search_tip':self.row_search.get_context(),
            #'director_name': self.get_director_name(),#model_to_name(self.model),
            #'ops' : self.get_operation()
        #} 
    
    def get_data_context(self): 
        return {
            'rows': self.get_rows(),
            'row_pages' : self.pagenum.get_context(),  
            'search_args':self.search_args
        } 
    
    def get_operation(self): 
        return []
    
    class pagenator(PageNum):
        #def __init__(self,pageNumber=1,perpage=None,kw={}):
            #self.pageNumber = int(pageNumber)
            #if perpage:
                #self.perPage= int(perpage) 
                
        def  get_context(self): 
            return {
                'crt_page':1,
                'total':1,
                'perpage':20
            }
    
    
