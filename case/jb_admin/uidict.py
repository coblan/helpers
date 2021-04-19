from helpers.maintenance.update_static_timestamp import static_url
from django.utils.translation import ugettext as _

def op_excel(max_length=2000,default_length=1000,length=None):
    if length:
        action ='''cfg.confirm("%(msg)s").then(()=>{
                       scope.ps.export_excel({count:%(length)s}) 
                     })'''%{'length':length,"msg":_('确定要导出EXCEL?')}
    else:
        action ='''cfg.prompt({title:"%(title)s",value:%(default_length)s}).then((value)=>{
                       if( isNaN(value) || value<0 || value >%(max_length)s){ alert("%(alert)s")}
                    else {
                       scope.ps.export_excel({count:value}) 
                    }
                     })
                   '''%{'max_length':max_length,
                        'default_length':default_length,
                        'title':_("导出最大条数"),
                        'alert':_("请输入小于%s的正整数"%max_length)}
    dc = {'editor':'com-slot-wrap',
                     'inn_editor':'com-btn',
                     'label':_('导出Excel'),
                     'click_express':action,
                     'slot':[
                         {'name':'content','html':'<img style="height: 20px;vertical-align: baseline;margin: -5px;" src="%(src)s" /><span>%(export_msg)s</span>'%{'src':static_url('jb_admin/image/excel-01.png'),'export_msg':_('导出Excel') }   }
                     ]
         }
    return dc
