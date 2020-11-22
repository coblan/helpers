
from django.conf import settings
from django.db import models

if getattr(settings,'DB_FULL_SEARCH',False) and  \
   settings.DATABASES['default']['ENGINE'] =='django.db.backends.mysql':
    class Search(models.Lookup):
        "mysql的全文搜索"
        lookup_name = 'search'
    
        def as_mysql(self, compiler, connection):
            lhs, lhs_params = self.process_lhs(compiler, connection)
            rhs, rhs_params = self.process_rhs(compiler, connection)
            params = lhs_params + rhs_params
            return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params
    
    models.CharField.register_lookup(Search)
    models.TextField.register_lookup(Search)