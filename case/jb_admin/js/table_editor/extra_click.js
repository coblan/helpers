/*
额外的点击列，例如“详情”
head['label']=
head['fun']

现在全部使用  com-table-ops-cell 控件

* */


var extra_click={
    props:['rowData','field','index'],
    template:`<span class="clickable" v-text="head.label" @click="on_click()"></span>`,
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
            this.$emit('on-custom-comp',{name:this.head.fun,row:this.rowData,head:this.head})
        }

    }
}

Vue.component('com-table-extraclick',extra_click)
