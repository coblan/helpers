/*
废弃了，采用 cfg.pop_middle('local-panel',ctx,callbank)
* */

// import {fields_all_in_one} from '../misc/form_one'
// 2023-12-1日改为引入formOne。注释掉了../misc/form_one.js文件，如果后面调试不通，可以恢复 form_one.js文件
import formOne from "../misc/formOne.vue";
Vue.component('com-local-form-one',{
    // mixins:[fields_all_in_one],
    mixins:[formOne],
    methods:{
        save:function(){
            //cfg.show_load()
            if(this.isValid()){
                this.$emit('finish',{row:this.row,vc:this})
            }
            // 该组件应该会被移除掉。这里暂时补充返回一个 promise ,以免造成报错
            return new Promise((resolve,reject)=>{
                resolve(this.row)
            })
        }
    }
})

function pop_edit_local(row,fields_ctx,callback,layerConfig){

    //var no_sub_to_server={
    //    methods:{
    //        save:function(){
    //            //cfg.show_load()
    //            if(this.isValid()){
    //                this.$emit('submit-success',this.row)
    //            }
    //            // 该组件应该会被移除掉。这里暂时补充返回一个 promise ,以免造成报错
    //           return new Promise((resolve,reject)=>{
    //               resolve(this.row)
    //           })
    //        }
    //    }
    //}

    //if(!fields_ctx.extra_mixins){
    //    fields_ctx.extra_mixins =[no_sub_to_server]
    //}else{
    //    fields_ctx.extra_mixins= [no_sub_to_server] .concat(fields_ctx.extra_mixins)
    //}
    fields_ctx.row=row
    fields_ctx.ops_loc = 'bottom'
   var openfields_layer_index = pop_layer(fields_ctx,'com-local-form-one',callback,layerConfig)  //  pop_fields_layer(row,fields_ctx,callback,layerConfig)
    return openfields_layer_index

}
//window.no_sub_to_server=no_sub_to_server
window.pop_edit_local = pop_edit_local