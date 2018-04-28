/*
 额外的点击列，例如“详情”
 * */

/*
* head={
*
* }
* */
var operations={
    props:['rowData','field','index'],
    template:`<div>
        <span style="margin-right: 1em" v-for="op in head.operations" v-show="! rowData['_op_'+op.name+'_hide']" class="clickable" v-text="op.label" @click="on_click()"></span>
    </div>`,
    created:function(){
        // find head from parent table
        var table_par = this.$parent
        while (true){
            if (table_par.heads){
                break
            }
            table_par = table_par.$parent
            if(!table_par){
                break
            }
        }
        this.table_par = table_par
        this. head  = ex.findone(this.table_par.heads,{name:this.field})
    },
    methods:{
        on_click:function(){
            this.$emit('on-custom-comp',{name:this.head.extra_fun,row:this.rowData})
        }

    }
}

Vue.component('com-table-operations',operations)
