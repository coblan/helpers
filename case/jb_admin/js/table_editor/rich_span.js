
var label_shower = {
    props:['rowData','field','index'],
//:class="myclass"
template:`<div :class="['com-table-rich-span',myclass]" >
 <component v-if="head.inn_editor"
            :is="head.inn_editor"
            :row-data="rowData" :field="field" :index="index"></component>
            <span v-else v-text="show_text"></span>
</div>`,
    created(){
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
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
        this.on_row_change()
    },
    watch:{
        rowData:{
            handler(v){
                this.on_row_change()
            },
            deep:true
        }
    },
    methods:{
        on_row_change(){
            if(this.head.row_change_express){
                ex.eval(this.head.row_change_express,{row:this.rowData,head:this.head,td:$(this.$el).parents('td').first()})
            }
        }
    },
    computed:{
        show_text:function(){
            var value = this.rowData[this.field]
            if( value == undefined){
                return ''
            }else if(typeof value == 'object'){
                return JSON.stringify(value)
            } else{
                return this.rowData[this.field]
            }
        },
        myclass(){
            if(this.head.cell_class){
                return ex.eval(this.head.cell_class,{row:this.rowData,head:this.head})
            }else{
                return ''
            }
        }
    }
}

Vue.component('com-table-rich-span',label_shower)
