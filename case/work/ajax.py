from helpers.director.db_tools import from_dict
from .admin import WRselfForm



def save_workself(row,user,request):
    #instance=from_dict(row)
    fm = WRselfForm(row,crt_user=user,request=request)
    if fm.is_valid():
        fm.save_form()
        return {'status':'success'}
    else:
        return {'errors':dict(fm.errors)}

def get_global():
    return globals()