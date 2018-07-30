var no_sub_to_server={
    methods:{
        submit:function(){
            this.$emit('sub_success',this.row)
        },
        save:function(){
            cfg.show_load()
            this.$emit('sub_success',{new_row:this.row})
            cfg.hide_load(2000)
        }
    }
}


function pop_edit_local(row,fields_ctx,callback){
    if(!fields_ctx.extra_mixins){
        fields_ctx.extra_mixins =['no_sub_to_server']
    }else{
        fields_ctx.extra_mixins= ['no_sub_to_server'] .concat(fields_ctx.extra_mixins)
    }

    pop_fields_layer(row,fields_ctx,callback)

}
window.no_sub_to_server=no_sub_to_server
window.pop_edit_local = pop_edit_local