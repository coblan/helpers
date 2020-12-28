export var obj_control={
    isEmpty:function(obj){
        if(typeof(obj)=='object'){
            var keys =Object.keys(obj)
            return keys.length == 0
        }else{
            return true
        }

        //for(var k in obj){
        //    if(/^[^_]/.exec(k)){
        //        return false
        //    }
        //}
        //return true
    },
    objContain(par,child){
        var is_contain = true
        for(var k in child){
            if(child[k] != par[k]){
                is_contain=false
                break
            }
        }
        return is_contain
    },
    mergeObject(dst,src){
        for(var k in src){
            if(dst[k] && src[k] && typeof(src[k])=='object'&& !Array.isArray(dst[k])&&!Array.isArray(src[k]) &&typeof(src[k])==typeof(dst[k]) ){
                ex.mergeObject(dst[k],src[k])
            }else{
                dst[k]=src[k]
            }
        }


        //if(Array.isArray(dst)){
        //    ex.each(dst,dst_item=>{
        //        ex.mergeObject()
        //    })
        //}
    },
    update_row(row){
        return ex.director_call('d.get_row',{pk:row.pk,director_name:row._director_name}).then((rt_row)=>{
            ex.vueAssign(row,rt_row)
        })
    }
}