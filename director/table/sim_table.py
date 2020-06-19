from .table import ModelTable, PageNum,evalue_container

class SimTable(ModelTable):
    """
    一般用于，与model不相关的table
    现在又plaintable了，这个模块无用了。
    """
    def __init__(self, _page=1, row_sort=[], row_filter={}, row_search='', crt_user=None, perpage=None, **kw): 
        self.search_args = kw.get('search_args')
        
        self.kw=kw
        self.crt_user=crt_user 
        self.page=_page
        self.footer = {}
        allowed_names= []  #self.permited_fields()
        
        self.row_sort=self.sort(row_sort,crt_user,allowed_names,kw)
        self.row_filter=self.filters(row_filter, crt_user, allowed_names,kw) 
        self.row_search = self.search( row_search,crt_user,allowed_names,kw)
        self.pagenum = self.pagenator(pageNumber=self.page,perpage=perpage)
    
    def get_heads(self): 
        return []

    #def get_data_context(self): 
        #return {
            #'rows': self.get_rows(),
            #'row_pages' : self.pagenum.get_context(),  
            #'search_args':self.search_args
        #} 
    
    def get_context(self):
        director_name =self.get_director_name()
        heads = self.get_heads()
        rows = self.get_rows()
        row_sort = self.row_sort.get_context()
        ops = self.get_operation()
        return {
            'heads':heads,
            'rows': rows,
            'row_pages' : self.getRowPages(),
            'row_sort':row_sort,
            'row_filters':  evalue_container( self.getRowFilters() ), #ls,
            #'search_tip':self.row_search.get_context(),
            'director_name':director_name,
            'ops' : ops,
            'search_args':self.search_args, 
            'parents': self.getParents(),
            'footer': self.footer,
        }    
    
    def get_operation(self): 
        return []
    
    class pagenator(PageNum):

        def  get_context(self): 
            return {
                'crt_page':1,
                'total':1,
                'perpage':20
            }
    
    
