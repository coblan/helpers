from django.utils.deprecation import MiddlewareMixin


class CrossSiteControl(MiddlewareMixin):
    def process_response(self,request,response):
        response['Access-Control-Allow-Origin'] = '*' #request.META.get('HTTP_HOST')
        response['Access-Control-Allow-Headers'] = 'X-Requested-With'
        response['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        response['Access-Control-Allow-Credentials'] = 'true'

        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
