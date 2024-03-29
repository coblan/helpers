export function save_row(row){
    // 直接保存 director modelfields  row 的数据，
    // 可能可以提取到ex接口里面
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
                        cfg.show_load()
                       return  ex.director_get(row._director_name, {pk: row.pk}).then(resp=> {
                           cfg.hide_load()
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