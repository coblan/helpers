# encoding:utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import inspect
from helpers.director.port import jsonpost
from helpers.common.dir_man import DirMan
from .models import Department

def manage_department(request):
    manager=DirMan(Department)
    scope= dict(inspect.getmembers(manager,inspect.ismethod))
    return jsonpost(request, scope)