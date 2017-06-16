# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.engine import BaseEngine,can_list,can_touch,fa,page,and_list
from .models import WorkRecord,Work,Index
from helpers.director.shortcut import ModelPermit


def can_check_work(user):
    permit=ModelPermit(WorkRecord, user)
    return 'status' in permit.changeable_fields()

def can_create_work(user):
    permit=ModelPermit(WorkRecord, user)
    return permit.can_add()

pc_menu= {'label':'工作统计','icon':fa('fa-users'),'visible':can_list((Work,WorkRecord,Index)),
         'submenu':[{'label':'工作类别','url': page('work.workindex'),'visible':can_list([Work,Index])},
                    {'label':'工作记录','url':page('work.workrecord'),'visible':can_touch(WorkRecord)}
                    ]
         }

wx_menu=[
    {'label':'工作类别','url':page('work.workindex.wx'),'icon':'<img src="/static/res/image/work_types.ico" />','visible':can_list((Work,WorkRecord,Index))}, 
    {'label':'个人工作提交','url':page('work.wkself.wx'),'icon':fa('fa-list-ol fa-2x'),'visible':and_list([can_create_work])},  
    {'label':'工作审核','url':page('work.workrecord'),'icon':fa('fa-check-square-o fa-2x'),'visible':and_list(
        [WorkRecord,can_check_work])},  

    {'label':'工作记录','url':page('work.worklist.wx'),'icon':fa('fa-calendar-check-o fa-2x'),'visible':and_list(['work.check_all'])},     
]
    

