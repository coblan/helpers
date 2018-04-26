from helpers.director.base_data import js_tr_list
from django.utils.translation import ugettext as _

def get_tr():
    return {
        'base_setting':_('Basic Setting'),
        'language':_('Language'),
        'back':_('back'),
        'search':_('Search'),
        'change_password':_('Change Password'),
        'logout':_('LogOut'),
        'login':_('LogIn'),            
    }

js_tr_list.append(get_tr)
