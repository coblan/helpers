export function save_row(row){
    var p = new Promise((resolve,reject)=>{
      return  ex.director_call('d.save_row',{row:row}).then( (resp) =>{
            var rt = resp //resp.save_row
            if(rt.errors){
               cfg.showMsg(rt.errors)
                reject()
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
                reject()
            }else{
                resolve(rt.row )
            }
        }).catch(()=>{
          reject()
      })
    })
    return p
}