from elasticsearch import Elasticsearch
import logging
import socket
import datetime
import sys

import logging
general_log = logging.getLogger('general_log')

class ELKHander(logging.Handler):
    host=''
    user=''
    pswd=''
    index=''
    def __init__(self):
        self.es = Elasticsearch(self.host,http_auth=(self.user,self.pswd ),)
        self.make_index()
        self.hostName = socket.gethostname()
        super().__init__()
        #print('elk-log1')
        
    def make_index(self):
        _index_mappings = {
            "mappings": {
                "properties": { 
                  "@timestamp":    { "type": "date"  }, 
                  "level":     { "type": "text"  }, 
                  "host": {"type": "text"},
                  "message":      { "type": "text" }, 
                }
            }
          }
        if self.es.indices.exists(index= self.index ) is not True:
            res = self.es.indices.create(index = self.index, body=_index_mappings) 
    
    def emit(self, record): 
        msg =   record.getMessage()
        if record.levelname == 'ERROR':
            if record.exc_text:
                msg += '\n' + record.exc_text
        dc = {
            '@timestamp': datetime.datetime.utcnow(),
            'level': record.levelname,
            'host': self.hostName,
            'message': msg
        }
        try:
            res = self.es.index(self.index, doc_type='_doc', body = dc,request_timeout=30)
        except Exception as e:
            general_log.error('请求ELK出现了问题msg=%(msg)s,Exception= %(except)s' % {'msg':msg,'except':str(e)})



