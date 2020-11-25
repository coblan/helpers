from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection

class Command(BaseCommand):
    """
    日志的全文搜索。需要在mysql 5.7以上才能用。限制了它的使用，展示放在这里，作为样例
    """
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            #cursor.execute('''drop index message_full
    #on act_log_generallog;''')
            #cursor.execute('''drop index content_full
    #on act_log_backendoperation;''')            
            
            cursor.execute('''alter table act_log_generallog
    add fulltext index message_full(message) WITH PARSER ngram;''')  
            cursor.execute('''alter table act_log_backendoperation
    add fulltext index content_full(content) WITH PARSER ngram;''')              

# 某个地方引入
#from django.db import models

#class Search(models.Lookup):
    #"mysql的全文搜索"
    #lookup_name = 'search'

    #def as_mysql(self, compiler, connection):
        #lhs, lhs_params = self.process_lhs(compiler, connection)
        #rhs, rhs_params = self.process_rhs(compiler, connection)
        #params = lhs_params + rhs_params
        #return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params

#models.CharField.register_lookup(Search)
#models.TextField.register_lookup(Search)


# 查询的时候用  field__search  进行全文查询
#def clean_search_args(self, search_args):
    #if search_args.get('message'):
        #if settings.DATABASES['default']['ENGINE'] =='django.db.backends.mysql':
            #search_args['message__search'] = search_args.pop('message')
    #return search_args