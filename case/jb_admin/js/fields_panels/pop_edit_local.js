/*
废弃了，采用 cfg.pop_middle('local-panel',ctx,callbank)
* */



function pop_edit_local(row,fields_ctx,callback,layerConfig){

    var no_sub_to_server={
        methods:{
            save:function(){
                //cfg.show_load()
                if(this.isValid()){
                    this.$emit('submit-success',this.row)
                }
                //cfg.hide_load(2000)
            }
        }
    }

    if(!fields_ctx.extra_mixins){
        fields_ctx.extra_mixins =[no_sub_to_server]
    }else{
        fields_ctx.extra_mixins= [no_sub_to_server] .concat(fields_ctx.extra_mixins)
    }
   var openfields_layer_index =  pop_fields_layer(row,fields_ctx,callback,layerConfig)
    return openfields_layer_index

}
//window.no_sub_to_server=no_sub_to_server
window.pop_edit_local = pop_edit_local