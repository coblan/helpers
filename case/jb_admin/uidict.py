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


def pop_edit_current_row():
    return ''' scope.head.fields_ctx.genVc=scope.vc;
                scope.head.fields_ctx.title=scope.row._label;
                scope.head.fields_ctx.par_row=scope.row;
                scope.head.fields_ctx.row = ex.copy(scope.row); // [1] 如果不是编辑par_row ，可以修改这行
                cfg.pop_vue_com("com-form-one" ,scope.head.fields_ctx)'''
    
    #head['fields_ctx'] = fields_ctx
    #head['fields_ctx'].update({
        ##'after_save':'scope.vc.par_row.car_no =scope.row.car_no; scope.vc.par_row.has_washed=scope.row.has_washed ',
        ##'init_express':'cfg.show_load(),ex.director_call(scope.vc.ctx.director_name,{pk:scope.vc.par_row.pk}).then((res)=>{cfg.hide_load();ex.vueAssign(scope.row,res.row)})',
       
        ##'mounted_express':'ex.vueAssign(scope.row,scope.vc.par_row)',
        ##'after_save':'ex.vueAssign( scope.vc.par_row,scope.row)',
        #'ops_loc':'bottom',
        ## 把初始化row放到 action里面去了 [1]
        ##'mounted_express':'ex.vueAssign(scope.row,ex.copy(scope.vc.par_row))',
        #})
    
    #head.update({
        #''
        #'click_express':
    #})