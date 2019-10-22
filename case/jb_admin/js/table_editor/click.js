
var my_click = {
    // head: {fun:'xxx'}
    props:['rowData','field','index'],
    template:`<div class="com-table-click clickable" @click="on_click()" style="display: inline-block">
        <component v-if="head.inn_editor"
            :is="head.inn_editor"
            :row-data="rowData" :field="field" :index="index"></component>
        <span v-else="" v-text="rowData[field]" ></span>
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

        this.parStore = ex.vueParStore(this)
    },
    methods:{
        on_click:function(){
            ex.eval(this.head.action,{row:this.rowData,head:this.head,ps:this.parStore})
            //this.$emit('on-custom-comp',{name:this.head.fun,row:this.rowData,head:this.head})
        }
    }
}

Vue.component('com-table-click',my_click)
