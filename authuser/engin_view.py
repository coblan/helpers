from helpers.director.engine import BaseEngine,page,fa,can_list,can_touch
from . base_data import auth_page_dc
from django.conf import settings
from helpers.func.dot_dict import read_dict_path

class AuthEngine(BaseEngine):
    url_name = 'authengine'
    need_login = False
    need_staff = False
    access_from_internet = True
    forbid_pages = read_dict_path(settings,'AUTHUSER.forbid_pages',[])
    


AuthEngine.add_pages(auth_page_dc)