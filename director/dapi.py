from helpers.director.ajax import save_row
from helpers.director.decorator import get_request_cache
from django.http import JsonResponse
from .shortcut import director_view
from helpers.director.base_data import director
from .model_func.wirtedb import permit_save_model

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

@director_view('get_row')
def get_row(director_name,filter_kws={}):
     fields_cls = director.get(director_name)
     fields_obj = fields_cls(**filter_kws)
     return fields_obj.get_row()

@director_view('save_rows')
def save_rows(rows):
     request = get_request_cache()['request']
     user = request.user
     ls =[]
     try:
          for row in rows:
               field_obj = permit_save_model(user, row)
               dc = field_obj.get_row() 
               ls.append(dc)
          return ls
     
     except ValidationError as e:
          return {'errors':dict(e),}   