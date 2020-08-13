export function save_row(row){
    var p = new Promise((resolve,reject)=>{
        ex.director_call('d.save_row',{row:row}).then( (resp) =>{

            var rt = resp //resp.save_row
            if(rt.errors){
               cfg.showMsg(rt.errors)
            }else if(rt._outdate){
                cfg.outdate_confirm(
                    rt._outdate,
                    function() {
                        ex.director_call(row._director_name, {pk: row.pk}).then(resp=> {
                            ex.vueAssign(row, resp.row)
                        })
                    },function(){
                        row.meta_overlap_fields='__all__'
                        save_row(row)
                    }
                )
            }else{
                //ex.vueAssign(row,rt.row)
                resolve(rt.row)
            }
        })
    })
    return p
}