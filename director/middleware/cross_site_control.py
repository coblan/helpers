from django.utils.deprecation import MiddlewareMixin


class CrossSiteControl(MiddlewareMixin):
    def process_response(self,request,response):
        response['Access-Control-Allow-Origin'] = '*'
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
