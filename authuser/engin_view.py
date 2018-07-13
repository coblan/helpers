from helpers.director.engine import BaseEngine,page,fa,can_list,can_touch
from . page import auth_page

class AuthEngine(BaseEngine):
    url_name = 'authengine'
    need_login = False
    


AuthEngine.add_pages(auth_page)