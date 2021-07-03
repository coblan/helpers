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
    template:`<div class="com-table-ops-cell">
        <!--<span style="margin-right: 1em" v-for="op in head.operations" v-show="! rowData['_op_'+op.name+'_hide']" class="clickable" v-text="op.label" @click="on_click()"></span>-->
        <component v-for="op in normed_heads" :is="op.editor" :head="op" @operation="on_operation($event)"></component>
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
    data:function(){
        var self=this
        var childStore= new Vue()
        childStore.vc = this
        return {
            childStore:childStore
        }
    },
    mounted:function(){
        this.parStore = ex.vueParStore(this)
    },
    computed:{
        normed_heads(){
            return ex.filter(this.head.ops,item=>{
                if(item.show_express){
                    return ex.eval(item.show_express,{vc:this})
                }else{
                    return true
                }
            })
        }
    },
    methods:{
        on_operation:function(op){
            if(op.action){
                ex.eval(op.action,{ps:this.parStore,head:this.head,row:this.rowData})
            }
        },
        //on_click:function(op){
        //    if(op.action){
        //        ex.eval(op.action,{ps:this.parStore,head:this.head,row:this.rowData})
        //    }
        //}

    }
}

Vue.component('com-table-ops-cell',operations)
