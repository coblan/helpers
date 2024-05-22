from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

class CrossSiteControl(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'OPTIONS':
           #response['Access-Control-Allow-Headers'] = 'Content-Type'
            response =HttpResponse()
            #response['Access-Control-Allow-Origin'] = '*' #request.META.get('HTTP_HOST')
            #response['Access-Control-Allow-Headers'] = 'X-Requested-With'
            #response['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
            #response['Access-Control-Allow-Credentials'] = 'true'                
            response.status_code= 204
            return response
                
    def process_response(self,request,response):
        response['Access-Control-Allow-Origin'] = '*' #request.META.get('HTTP_HOST')
        #response['Access-Control-Allow-Headers'] = 'X-Requested-With'
        response['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Headers'] ='DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';

        #if request.method == 'OPTIONS':
            ##response['Access-Control-Allow-Headers'] = 'Content-Type'
            #response.status_code= 204
        return response
