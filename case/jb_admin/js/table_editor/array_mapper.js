/*
将 pk 数组映射为 label字符串
[1,2,3] -> '小王;小张;小赵'

* */
import {find_par} from './table_funs/common'
var array_mapper = {
    props:['rowData','field','index'],
    template:`<span v-text="show_data"></span>`,
    //created:function(){
    //    // find head from parent table
    //    var table_par = this.$parent
    //    while (true){
    //        if (table_par.heads){
    //            break
    //        }
    //        table_par = table_par.$parent
    //        if(!table_par){
    //            break
    //        }
    //    }
    //    this.table_par = table_par
    //    this.head = ex.findone(this.table_par.heads,{name:this.field})
    //},
    data(){
        find_par(this)
        //var table_par = this.$parent
        //while (true){
        //    if (table_par.heads){
        //        break
        //    }
        //    table_par = table_par.$parent
        //    if(!table_par){
        //        break
        //    }
        //}
        //this.table_par = table_par
        //this.head = ex.findone(this.table_par.heads,{name:this.field})
      return {
          options: this.head. options
      }
    },
    mounted(){
        if(this.head.mounted_express){
            ex.eval(this.head.mounted_express,{vc:this,head:this.head,row:this.rowData})
        }
    },
    computed:{
        show_data:function(){
            var self=this
            var values = self.rowData[self.field]
            if(!values){
                return values
            }

            if(this.table_par){
                if(this.head.parse_input){
                    var values=parse_input[this.head.parse_input](values)
                }
                var value_labels=ex.map(values,function(value){
                    var item = ex.findone(self.options,{value:value})
                    if(item){
                        return item.label
                    }else{
                        return ''
                    }
                   // {value:value,label:self.head.options[value]}
                })
                var ordered_values = ex.sortOrder(value_labels)

                //var str =''
                //ex.each(ordered_values,function(itm){
                //    str+=itm.label
                //    //str+= options[itm]
                //    str+=';'
                //})
                return ordered_values.join(';')
                //return options[value]
            }
        },

    }
}

var parse_input={
    dotSplit:function(str){
        return str.split(',')
    },
}

Vue.component('com-table-array-mapper',array_mapper)
