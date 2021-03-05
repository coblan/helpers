from helpers.maintenance.update_static_timestamp import static_url
from django.utils.translation import ugettext as _

def op_excel(max_length=2000,length=None):
    if length:
        action ='''cfg.confirm("%(msg)s").then(()=>{
                       scope.ps.export_excel({count:%(length)s}) 
                     })'''%{'length':length,"msg":_('确定要导出EXCEL?')}
    else:
        action ='''cfg.prompt({title:"%(title)s",value:1000}).then((value)=>{
                       if( isNaN(value) || value<0 || value >%(max_length)s){ alert("%(alert)s")}
                    else {
                       scope.ps.export_excel({count:value}) 
                    }
                     })
                   '''%{'max_length':max_length,'title':_("导出最大条数"),'alert':_("请输入小于%(max_length)s的正整数")}
    dc = {'editor':'com-slot-wrap',
                     'inn_editor':'com-btn',
                     'label':_('导出Excel'),
                     'action':action,
                     'slot':[
                         {'name':'content','html':'<img style="height: 20px;vertical-align: baseline;margin: -5px;" src="%(src)s" /><span>%(export_msg)s</span>'%{'src':static_url('jb_admin/image/excel-01.png'),'export_msg':_('导出Excel') }   }
                     ]
         }
    return dc
