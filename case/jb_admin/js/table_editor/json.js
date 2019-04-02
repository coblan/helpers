Vue.component('com-table-json',{
    props:['rowData','field','index'],
    template:`<span class="com-table-json" v-text="show_text">
    </span>`,
    computed:{
        show_text:function(){
            if(this.rowData[this.field]) {
                return JSON.stringify(this.rowData[this.field] )
            }else{
                return ''
            }
        }
    }
})