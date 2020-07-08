
var tab_fields={
    props:['tab_head','par_row'],
    data(){
        var ctx = this.tab_head.fields_ctx
        ex.assign(ctx,{
            par_row:this.par_row,
            init_express:this.tab_head.init_express,
            mounted_express:this.tab_head.mounted_express,
        })
        return {
            ctx:ctx
        }
    },
    template:`<div class="com-tab-fields-v1 com-tab-fields com-tab-form" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;">
    <com-form-one :ctx="ctx"></com-form-one>
    </div>`,
    mounted(){
        // 滚动限制在 fields-area内，80是operation区域的高度
        //var par_height = $(this.$el).parents('.el-tabs__content').height()
        //$(this.$el).find('.fields-area').height(par_height - 80)
    }
}

Vue.component('com-tab-fields-v1',tab_fields)
Vue.component('com-tab-form',tab_fields)