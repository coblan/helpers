
var label_shower = {
    props:['rowData','field','index'],
    template:`<span v-text="show_text"></span>`,
    computed:{
        show_text:function(){
            return this.rowData[this.field] || ''
        }
    }
}

Vue.component('com-table-span',label_shower)
