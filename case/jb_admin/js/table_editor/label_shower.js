
var label_shower = {
    props:['rowData','field','index'],
    template:`<span v-text="show_text"></span>`,
    data:function(){
        return {
            label:'_'+this.field+'_label'
        }
    },
    computed:{
        show_text:function(){
            return this.rowData[this.label] || ''
        }
    }
}

Vue.component('com-table-label-shower',label_shower)
