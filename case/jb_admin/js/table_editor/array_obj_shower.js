
var array_mapper = {
    props:['rowData','field','index'],
    template:`<span v-text="show_data"></span>`,
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
        this.head = ex.findone(this.table_par.heads,{name:this.field})
    },
    computed:{
        show_data:function(){
            var self=this
            var values = self.rowData[self.field]
            if(!values){
                return values
            }
            var obj_list = JSON.parse(values)
            var out_list = ex.map(obj_list,function(item){
                return item[self.head.key|| 'label' ]
            })
            return out_list.join(';')
            }
        },

}


Vue.component('com-table-array-obj-shower',array_mapper)
