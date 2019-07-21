
/*
options:{
    key:value
}
* */
var mapper = {
    props:['rowData','field','index'],
    template:`<span class="com-table-mapper" v-text="show_data"></span>`,
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
        this.head= ex.findone(this.table_par.heads,{name:this.field})
    },
    //mounted(){
    //    if(this.head.css){
    //        ex.append_css(this.head.css)
    //    }
    //},
    computed:{
        //myclass(){
        //    if(this.head.class){
        //        return ex.eval(this.head.class,{head:this.head,row:this.rowData})
        //    }else{
        //        return ''
        //    }
        //},
        show_data:function(){
            if(this.table_par){
                var value = this.rowData[this.field]
                var options = this.head.options
                var opt = ex.findone(options,{value:value})
                if(opt){
                    return opt['label']
                }else{
                    return value
                }
            }

        }
    }
}

Vue.component('com-table-mapper',mapper)
