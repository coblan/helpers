
/*
options:{
    key:value
}
* */
var mapper = {
    props:['rowData','field','index'],
    template:`<span class="com-table-mapper" v-text="show_data"></span>`,
    beforeCreate(){
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
        //this.heads =
        //this.head= ex.findone(this.table_par.heads,{name:this.field})
    },
    data(){
        this.head= ex.findone(this.table_par.heads,{name:this.field})
        return {
            options:this.head.options || [],
            parStore:ex.vueParStore(this)
        }
    },
    mounted(){
        if( this.head.mounted_express){
            ex.eval(this.head.mounted_express,{vc:this,})
        }
    },
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
                var options = this.options
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
