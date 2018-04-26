
var select = {
    props:['rowData','field','index'],
    template:`<div >
    <select style="width: 100%" @change="on_changed()"  v-model="rowData[field]">
        <option v-for="op in head.options" :value="op.value" v-text="op.label"></option>
    </select>
    </div>`,
    data:function(){
        return {
        }
    },
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
        on_changed:function(){
            this.$emit('on-custom-comp',{name:'row_changed',row:this.rowData})
        }
    }
}

Vue.component('com-table-select',select)
