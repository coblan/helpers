#from helpers.director.ajax import save_row
from helpers.director.decorator import get_request_cache
from django.http import JsonResponse
from .shortcut import director_view
from helpers.director.base_data import director
from .model_func.wirtedb import permit_save_model
from django.core.exceptions import ValidationError
from .fields.fields import ModelFields,OutDateException
from django.core.exceptions import PermissionDenied
from .model_func.dictfy import delete_related_query
from .base_data import director_transaction 
from django.db import transaction
from . views import tranactionDbs
from django.utils import timezone
from django.http import Http404
import os
from django.conf import settings
from helpers.director.base_data import exclude_transaction

def director_save_row(row):
     #rt_dc = save_row(row,user,request)
     rt_dc = save_row(row)
     if 'errors' in rt_dc:
          errors = {}
          for k,v in rt_dc['errors'].items():
               errors[k] = ';'.join(v)
          return JsonResponse({'success':False,'msg':'字段验证错误','data':errors})
     else:
          return {}

#def _total_save(user, row,**kw):
     #field_obj = permit_save_model(user, row,**kw)
     #dc = field_obj.get_row()
     #return dc

@director_view('d.save_row')
def save_row(row):
     request = get_request_cache()['request']
     user = request.user
     try:
          kw = request.GET.dict()
          #[1] 下面本来用来控制事务的，不过现在使用db_router来控制
          #d_name =  row.get('_director_name')
          #if director_transaction.get(d_name):
               #real_save = tranactionDbs(_total_save,director_transaction.get(d_name))
               #dc = real_save(user, row,**kw)
          #else:
               #dc = _total_save(user, row,**kw)
          # [1] 直接使用下面代码
          field_obj = permit_save_model(user, row,**kw)
          dc = field_obj.get_row()
          
          return {'success':True,'status':'success','row':dc}
     except ValidationError as e:
          return {'errors':dict(e)}
     except PermissionDenied as e:
          raise UserWarning(str(e))
     except OutDateException as e:
          return {'_outdate':str(e)}


@director_view('d.save_row_for_front')
def save_row_for_front(row):
     request = get_request_cache()['request']
     user = request.user
     try:
          # 记录下director 的form，后面报错会根据form类确定是否报异常到前端。
          # 如果这里不记录，经过permit_save_model后，row可能没有_director_name属性了。
          fields_cls = director.get(row['_director_name'])
          
          kw = request.GET.dict()
          field_obj = permit_save_model(user, row,**kw)
          dc = field_obj.get_row()
          return dc
     except ValidationError as e:
          if getattr(fields_cls,'front_info',True):
               return {'errors':dict(e)}
          else:
               raise UserWarning(dict(e))
     except PermissionDenied as e:
          raise UserWarning(str(e))
     except OutDateException as e:
          if getattr(fields_cls,'front_info',True):
               return {'_outdate':str(e)}
          else:        
               raise UserWarning(str(e))


@exclude_transaction
@director_view('d.get_row')
@director_view('get_row')
def get_row(director_name,pk=None,**kws):
     fields_cls = director.get(director_name)
     fields_obj = fields_cls(pk=pk,select_for_update=False, **kws)
     return fields_obj.get_row()

@exclude_transaction
@director_view('d.get_row_form_db')
def get_row_form_db(rows):
     out_rows = [get_row(row.get('_director_name'),row.get('pk')) for row in rows]
     return out_rows

@exclude_transaction
@director_view('d.get_rows')
def get_rows(director_name,search_args={},user=None):
     table_cls = director.get(director_name)
     table_obj = table_cls.gen_from_search_args(search_args,user)
     return table_obj.get_data_context()

@director_view('save_rows')
@director_view('d.save_rows')
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
     except OutDateException as e:
          return {'_outdate':str(e)}
     except PermissionDenied as e :
          raise UserWarning(str(e))

@exclude_transaction
@director_view('d.get_head_context')
def get_head_context(director_name):
     dcls = director.get(director_name)
     return dcls(select_for_update=False).get_head_context()

@exclude_transaction
@director_view('d.get_context')
def get_context(director_name):
     dcls = director.get(director_name)
     return dcls(select_for_update=False).get_context()

#@exclude_transaction
@director_view('d.director_element_call')
def director_element_call(director_name,attr_name,kws):
     dcls = director.get(director_name)
     obj = dcls()
     return getattr(obj,attr_name)(**kws)

# [1] 新开一个d.director_element_call，给dapi用，不去修改老的，免得引起其他问题
@director_view('d.director_element_call2')
def director_element_call(director_name,attr_name,**kws):
     dcls = director.get(director_name)
     obj = dcls()
     if hasattr(obj,'public_api') and attr_name not in obj.public_api:
          raise Http404()   
     return getattr(obj,attr_name)(**kws)

@director_view('d.delete_query_related')
def search_delete_related(rows):
     out_ls =[]
     for row in rows:
          fields_cls = director.get(row['_director_name'])
          fields_obj = fields_cls(dc = row,select_for_update=False)
          inst = fields_obj.instance
          ls = delete_related_query(inst)
          if ls:
               out_ls.append(
                    {'str':str(inst),'related':ls}
               )
     return out_ls


@director_view('d.delete_rows')
def del_rows(rows):
     for row in rows:
          fields_cls = director.get(row.get('_director_name'))
          fields_obj = fields_cls(row,select_for_update=True)
          fields_obj.del_form()
     rows_only_pk=[{'pk':x['pk']} for x in rows]
     return rows_only_pk

@director_view('d.delete_row')
def del_rows(row):
     fields_cls = director.get(row.get('_director_name'))
     fields_obj = fields_cls(row,select_for_update=True)
     fields_obj.del_form()

@director_view('d.gen_excel')
def get_excel(director_name,search_args): 
     table_cls = director.get(director_name)
     table_obj = table_cls.gen_from_search_args(search_args)
     wb = table_obj.get_excel()
     fl_name = director_name.replace('.', '_')
     now = timezone.now().strftime('%Y_%m_%d_%H_%M_%S')
     fl_name =  '%s_%s.xlsx' % (fl_name, now)

     wb.save(filename = os.path.join(settings.MEDIA_ROOT, 'gen_files', fl_name))
     return {'file_url': '/media/gen_files/%s' % fl_name,}