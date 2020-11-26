import logging
operation_log_ = logging.getLogger('operation')
from helpers.director.shortcut import get_request_cache
import json

def operation_log(content_or_dc):
    user = get_request_cache()['request'].user
    if user.is_anonymous():
        op_user = ''
    else:
        op_user = str(user)
    if isinstance(content_or_dc,dict):
        dc = content_or_dc
    else:
        dc = {
            'content':content_or_dc
        }
        
    dc.update({
        'user':str(user)
    })
    operation_log_.info( json.dumps(dc,ensure_ascii=False) )
