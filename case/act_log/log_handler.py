import logging
import socket
import datetime
from django.conf import settings
from helpers.director.middleware.request_cache import get_request_cache

import json

dc = {
}

class DBOperationHandler(logging.Handler):

    def emit(self, record): 
        global dc
        if not dc.get('BackendOperation'):
            from .models import BackendOperation
            dc['BackendOperation'] = BackendOperation
        BackendOperation = dc['BackendOperation']
        
        msg =   record.getMessage()
        if record.levelname == 'ERROR':
            msg += '\n' + record.exc_text
        
        user = get_request_cache().get('request').user
        user_label = user.username if user.is_authenticated else '【匿名用户】'
        
        try:
            db_op_dict = json.loads(msg)
           
            content = db_op_dict.pop('content', None)
            if not content:
                content = parser_form_log(db_op_dict)
            type_key = db_op_dict.pop('model', '')
            op= db_op_dict.pop('kind','')
            pk = db_op_dict.pop('pk','')
            BackendOperation.objects.create(createuser = user_label,
                                            inst_pk=pk,
                                            op=op,
                                          model = type_key, 
                                          content = content, 
                                          )            
        except json.decoder.JSONDecodeError:
            type_key = '_direct_message'
            #memo = ''
            content = msg
            BackendOperation.objects.create(createuser = user_label,
                                          model = type_key, 
                                          content = content, 
                                          )


def parser_form_log(dc): 
    after = dc.pop('_after', {})
    after.update( dc.pop('after', {}) )
    model = dc.get('model', '')
    pk = dc.get('pk', '')
    if after:
        before = dc.pop('_before', {})
        before.update( dc.pop('before', {}) )
        
        before_str =  ';'.join( ['%s=%s' % (k, v) for (k, v) in before.items()])
        after_str = ';'.join( ['%s=%s' % (k, v) for (k, v) in after.items()])
        str_kws =  {
            #'user': user,
            'pk': pk,
            'model': model,
            'before_str': before_str,
            'after_str': after_str,
        }
        if dc.get('kind') == 'add':
            content = '创建了主键为%(pk)s的%(model)s,值为%(after_str)s' % str_kws
        elif before_str:
            content = '将主键为%(pk)s的%(model)s,从%(before_str)s,修改为%(after_str)s' % str_kws
        else:
            content = '将主键为%(pk)s的%(model)s,修改为%(after_str)s' % str_kws
            
    else:
        content = json.dumps(dc)
    return content

        
