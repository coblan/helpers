Vue.component('com-table-label-shower',{
    props:['head','row'],
    template:`<span class="com-item-span-label" :class="cssclass" v-text="label_text"></span>`,
    computed:{
        label_text(){
            let key = '_'+this.head.name+'_label'
            return this.row[key]
        },
        cssclass(){
            if(this.head.class_express){
                return ex.eval(this.head.class_express,{row:this.row,head:this.head})
            }else{
                return this.head.class
            }
        }
    }
})