from helpers.director.engine import BaseEngine,page,fa,can_list,can_touch
from . base_data import auth_page_dc

class AuthEngine(BaseEngine):
    url_name = 'authengine'
    need_login = False
    need_staff = False
    access_from_internet = True
    


AuthEngine.add_pages(auth_page_dc)