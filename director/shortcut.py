from __future__ import absolute_import

from .model_admin.base import model_dc,model_page_dc,render_dc,permit_list
#from .model_admin.render import TablePage,FormPage
from .pages import TablePage,FormPage
from .model_admin.tabel import ModelTable,PageNum,TrivalPageNum
from .model_admin.fields import ModelFields,save_row
from .model_admin.permit import ModelPermit
from .container import evalue_container

