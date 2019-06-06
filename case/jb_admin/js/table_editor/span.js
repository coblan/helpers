
var label_shower = {
    props:['rowData','field','index'],
    template:`<span v-text="show_text"></span>`,
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
        }
    }
}

Vue.component('com-table-span',label_shower)
