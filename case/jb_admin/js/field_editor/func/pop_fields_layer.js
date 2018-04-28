/*
* root 层面创建Vue组件，形成弹出框
* */

export  function pop_fields_layer (row,heads,ops,callback){
    // row,head ->//model_name,relat_field


    //var relat_field = head.relat_field
    //var model_name = head.model_name
    //var ops = head.ops
    //if(dc.head.use_table_row){
    //    var lay_row = dc.row
    //}else{
    //    var lay_row ={}
    //}

    self.opened_layer_indx = layer.open({
        type: 1,
        area: ['700px', '400px'],
        title: '详细',
        resize:true,
        resizing: function(layero){
            var total_height= $('#fields-pop-'+pop_id).parents('.layui-layer').height()
             $('#fields-pop-'+pop_id).parents('.layui-layer-content').height(total_height-42)
        },
        shadeClose: true, //点击遮罩关闭
        content:`<div id="fields-pop-${pop_id}" style="height: 100%;">
                    <com-pop-fields @del_success="on_del()" @sub_success="on_sub_success($event)"
                    :row="row" :heads="fields_heads" :ops="ops"></com-pop-fields>
                </div>`
    });

    new Vue({
        el:'#fields-pop-'+pop_id,
        data:{
            row:row,
            fields_heads:heads,
            ops:ops
        },
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
}

window.pop_fields_layer = pop_fields_layer