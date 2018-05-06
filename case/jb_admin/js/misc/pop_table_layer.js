/*
 * root 层面创建Vue组件，形成弹出框
 * */

export  function pop_table_layer (row,table_ctx,callback){
    // row,head ->//model_name,relat_field


    var pop_id =new Date().getTime()

    self.opened_layer_indx = layer.open({
        type: 1,
        area: ['800px', '500px'],
        title: '列表',
        resize:true,
        resizing: function(layero){
            var total_height= $('#pop-table-'+pop_id).parents('.layui-layer').height()
            $('#pop-table-'+pop_id).parents('.layui-layer-content').height(total_height-42)
        },
        shadeClose: true, //点击遮罩关闭
        content:`<div id="pop-table-${pop_id}" style="height: 100%;">
                    <com-v-table ref="com_table" @del_success="on_del()" @sub_success="on_sub_success($event)"
                    :par_row="par_row" :table_ctx="table_ctx"></com-v-table>
                </div>`
    });


    new Vue({
        el:'#pop-table-'+pop_id,
        data:{
            par_row:row,
            table_ctx:table_ctx,
        },
        mounted:function(){
            this.$refs.com_table.getRows()
            var self =this
           //setTimeout(function(){
           //     self.$refs.com_table.getRows()
           // },1000)

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

window.pop_table_layer = pop_table_layer