
var label_shower = {
    props:['rowData','field','index'],
    template:`<span class="com-table-rich-span" :class="myclass" v-text="show_text"></span>`,
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
            if(this.head.class){
                return ex.eval(this.head.class,{row:this.rowData,head:this.head})
            }else{
                return ''
            }
        }
    }
}

Vue.component('com-table-rich-span',label_shower)
