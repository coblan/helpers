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
        self.footer = []
        allowed_names= []  #self.permited_fields()
        
        self.row_sort=self.sort(row_sort,crt_user,allowed_names,kw)
        self.row_filter=self.filters(row_filter, crt_user, allowed_names,kw) 
        self.row_search = self.search( row_search,crt_user,allowed_names,kw)
        self.pagenum = self.pagenator(pageNumber=self.page,perpage=perpage)
    

    #def get_data_context(self): 
        #return {
            #'rows': self.get_rows(),
            #'row_pages' : self.pagenum.get_context(),  
            #'search_args':self.search_args
        #} 
    
    def get_operation(self): 
        return []
    
    class pagenator(PageNum):

        def  get_context(self): 
            return {
                'crt_page':1,
                'total':1,
                'perpage':20
            }
    
    
