
var my_link = {
    props:['rowData','field','index'],
    template:`<div class="com-table-color" style="width:5em;height: 2em" :style="{background: rowData[field]}">

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
    data(){
        return {
            parStore:ex.vueParStore(this)
        }
    },

}

Vue.component('com-table-color',my_link)

