
var html_shower = {
    props:['rowData','field','index'],
    template:`<div :class="['com-table-map-html',head.class]" v-html="show_label"></div>`,
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
    },
    computed:{
        show_label(){
            var  value = this.rowData[this.field]
            if(this.head.map_express){
                return ex.eval(this.head.map_express,{head:this.head,row:this.rowData,})
            }
        }
    },
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
    }

}

Vue.component('com-table-map-html',html_shower)


