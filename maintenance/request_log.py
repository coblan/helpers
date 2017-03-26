import re
import logging
log = logging.getLogger('all_request')


class RequestMiddleware(object):
    #def process_request(self,request):
        #return request

    def process_response(self,request, response):
        url=request.get_full_path()
        content=response.content
        status_code=response.status_code
        if not re.search('application/json',response.get('Content-Type')):
            content= response.get('Content-Type') + ';Len:%s'%len(response.content)
       
        log.info('Url:{url}\nStatus_code:{status_code}\nContent:{content}'.format(url=url,content=content,status_code=status_code))
        return response