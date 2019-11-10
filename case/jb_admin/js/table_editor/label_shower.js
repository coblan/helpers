
var label_shower = {
    props:['rowData','field','index'],
    template:`<div class="com-table-label-shower" v-html="show_text"></div>`,
    data:function(){
        return {
            label:'_'+this.field+'_label'
        }
    },
    computed:{
        show_text:function(){
            if(this.rowData[this.label] != undefined){
                return this.rowData[this.label]
            }else{
                return ''
            }
        }
    }
}

Vue.component('com-table-label-shower',label_shower)
