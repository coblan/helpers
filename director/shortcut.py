from __future__ import absolute_import

from .model_admin.base import model_dc,page_dc,render_dc,permit_list
#from .model_admin.render import TablePage,FormPage
from .pages import TablePage,FormPage,TabGroup
from .model_admin.tabel import ModelTable,PageNum,TrivalPageNum,RowFilter,RowSearch,RowSort
from .model_admin.fields import ModelFields,save_row
from .model_admin.permit import ModelPermit,has_permit
from .container import evalue_container
from .short_gen import regist_director

