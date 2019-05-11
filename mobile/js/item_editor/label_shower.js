Vue.component('com-table-label-shower',{
    props:['head','row'],
    template:`<span class="com-item-span-label" v-text="label_text"></span>`,
    computed:{
        label_text(){
            let key = '_'+this.head.name+'_label'
            return this.row[key]
        }
    }
})