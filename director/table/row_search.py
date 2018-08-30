
from django.utils.translation import ugettext as _

class SelectSearch(object):
    names=[]
    exact_match = []
    model=''
    def __init__(self,q,user = None,allowed_names = [], kw = {}):
        self.valid_name= [x for x in self.names if x in allowed_names]
        self.crt_user=user
        self._names=[x for x in self.names if x in allowed_names]        
        self.q=q
        self.qf = kw.get('qf')
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
                'editor':'com-search-select',
                'name':'_q'
            }
            return dc
    
    def get_query(self,query):
        if self.q and self.qf:
            if self.qf in self.names:
                exp = {'%s__icontains'%self.qf: self.q,}
                return query.filter( **exp)
            elif self.qf in self.exact_match:
                exp = {self.qf, self.q}
                return query.filter( **exp)
        return query
