/*
将 pk 数组映射为 label字符串
[1,2,3] -> '小王;小张;小赵'
* */
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
            if(this.table_par){
                var values = self.rowData[self.field]
                var options =ex.map(values,function(value){
                   return{value:value,label:self.head.options[value]}
                })
                var ordered_values = ex.sortOrder(options,'label')
                var str =''
                ex.each(ordered_values,function(itm){
                    str+=itm.label
                    //str+= options[itm]
                    str+=';'
                })
                return str
                //return options[value]
            }

        }
    }
}

Vue.component('com-table-array-mapper',array_mapper)
