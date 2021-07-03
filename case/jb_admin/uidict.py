from helpers.maintenance.update_static_timestamp import static_url
from django.utils.translation import ugettext as _
import base64

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


def pop_edit_current_row():
    "在前端table中，弹出窗口编辑row"
    return ''' scope.head.fields_ctx.genVc=scope.vc;
                scope.head.fields_ctx.title=scope.row._label;
                scope.head.fields_ctx.par_row=scope.row;
                scope.head.fields_ctx.row = ex.copy(scope.row); // [1] 如果不是编辑par_row ，可以修改这行
                cfg.pop_vue_com("com-form-one" ,scope.head.fields_ctx)'''

def nice_express(express,msg):
    express = base64.b64encode(express.encode('utf-8'))
    msg = base64.b64encode(msg.encode('utf-8'))
    return'express(%s , %s)'%( express.decode('utf-8'),msg.decode('utf-8'))
