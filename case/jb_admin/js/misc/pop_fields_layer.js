/*
* root 层面创建Vue组件，形成弹出框
* */
import {com_pop_field} from  './com_pop_fields'

export  function pop_fields_layer (row,fields_ctx,callback){
    // row,head ->//model_name,relat_field

    var heads = fields_ctx.heads
    var ops = fields_ctx.ops
    var extra_mixins=fields_ctx.extra_mixins || []
    var com_fields = window[fields_ctx.fieldsPanel] || com_pop_field
    var com_id = md5(extra_mixins)
    if(! window['_vue_com_'+com_id]){
        extra_mixins = ex.map(extra_mixins,function(name){
            return window[name]
        })
        //var com_pop_field_real = $.extend({}, com_fields);
        //com_pop_field_real.mixins = com_fields.mixins.concat(extra_mixins)
        var com_pop_field_real =ex.vueExtend(com_fields,extra_mixins)
        Vue.component('com-pop-fields-'+com_id,com_pop_field_real)
        window['_vue_com_'+com_id] = true
    }

    var pop_id =new Date().getTime()

    self.opened_layer_indx = layer.open({
        type: 1,
        area: ['800px', '500px'],
        title: '详细',
        resize:true,
        resizing: function(layero){
            var total_height= $('#fields-pop-'+pop_id).parents('.layui-layer').height()
             $('#fields-pop-'+pop_id).parents('.layui-layer-content').height(total_height-42)
        },
        shadeClose: true, //点击遮罩关闭
        content:`<div id="fields-pop-${pop_id}" style="height: 100%;">
                    <component :is="'com-pop-fields-'+com_id" @del_success="on_del()" @sub_success="on_sub_success($event)"
                    :row="row" :heads="fields_heads" :ops="ops"></component>
                </div>`,
        end: function () {

            eventBus.$emit('openlayer_changed')

        }
    });

Vue.nextTick(function(){

    new Vue({
        el:'#fields-pop-'+pop_id,
        data:{
            has_heads_adaptor:false,
            row:row,
            fields_heads:heads,
            ops:ops,
            com_id:com_id,
        },
        //computed:{
        //    fields_heads:function(){
        //        if(this.has_heads_adaptor){
        //            return this.heads_adaptor(this.heads)
        //        } else{
        //            return this.heads
        //        }
        //    }
        //},
        mounted:function(){
            //if(! trigger.head.use_table_row){
            //    var self=this
            //    cfg.show_load()
            //    var dc ={fun:'get_row',model_name:model_name}
            //    dc[relat_field] = trigger.rowData[relat_field]
            //    var post_data=[dc]
            //    ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
            //        self.row = resp.get_row
            //        cfg.hide_load()
            //    })
            //}

        },
        methods:{
            on_sub_success:function(event){
                // 将新建的row 插入到表格中
                //if(! old_row.pk) {
                //    self.rows.splice(0, 0, new_row)
                //}
                //if(this.head.use_table_row){
                //    var old_row = event.old_row
                //    var new_row=event.new_row
                //    ex.assign(self.row,new_row)
                //}else{
                //    trigger.update_row()
                //}
                callback({name:'after_save',new_row:event.new_row,old_row:event.old_row})
                //eventBus.$emit('pop-win-'+pop_id,{name:'after_save',new_row:event.new_row,old_row:event.old_row})

            },
            //on_del:function(){
            //    ex.remove(self.rows,row)
            //    layer.close(self.opened_layer_indx)
            //},
        }
    })


    eventBus.$emit('openlayer_changed')


})


}

window.pop_fields_layer = pop_fields_layer