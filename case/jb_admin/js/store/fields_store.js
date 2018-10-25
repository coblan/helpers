var fields_store={
    state(){
        return {
            _rows_update_funcs:[],
        }
    },
    mutations:{
        regist_rows_update:function(state,func){
            state._rows_update_funcs.push(func)
        },
        rows_update:function(state,rows){
            ex.each(state._rows_update_funcs,function(func){
                func(rows)
            })
        },
    }
}