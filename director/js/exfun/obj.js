export var obj_control={
    isEmpty:function(obj){
        for(var k in obj){
            if(/^[^_]/.exec(k)){
                return false
            }
        }
        return true
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
    }
}