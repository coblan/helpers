
var tab_fields={
    props:['tab_head','par_row'],
    data(){
        var ctx = this.tab_head.fields_ctx
        ex.assign(ctx,{
            par_row:this.par_row,
            init_express:this.tab_head.init_express
        })
        return {
            ctx:ctx
        }
    },
    template:`<div class="com-tab-fields">
    <com-form-one :ctx="ctx"></com-form-one>
    </div>`
}

Vue.component('com-tab-fields-v1',tab_fields)