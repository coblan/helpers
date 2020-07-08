from helpers.maintenance.update_static_timestamp import static_url

def op_excel(max_length=2000):
    dc = {'editor':'com-slot-wrap',
                     'inn_editor':'com-btn',
                     'label':'导出Excel',
                     'action':'''cfg.prompt({title:"导出最大条数",value:1000}).then((value)=>{
                       if( isNaN(value) || value<0 || value >%(max_length)s){ alert("请输入小于%(max_length)s的正整数")}
                    else {
                       scope.ps.export_excel({count:value}) 
                    }
                     
                     })
                   '''%{'max_length':max_length},
                     'slot':[
                         {'name':'content','html':'<img style="height: 20px;vertical-align: baseline;margin: -5px;" src="%s" /><span>导出Excel</span>'%static_url('jb_admin/image/excel-01.png')}
                     ]
         }
    return dc


#//{
        #//    formType: 2,
        #//        value: '初始值',
        #//    title: '请输入值',
        #//    area: ['800px', '350px'] //自定义文本域宽高
        #//}