from helpers.director.ajax import save_row
from helpers.director.decorator import get_request_cache
from django.http import JsonResponse

def director_save_row(row):
     request = get_request_cache()['request']
     user = request.user
     rt_dc = save_row(row,user,request)
     if 'errors' in rt_dc:
          errors = {}
          for k,v in rt_dc['errors'].items():
               errors[k] = ';'.join(v)
          return JsonResponse({'success':False,'msg':'字段验证错误','data':errors})
     else:
          return {}