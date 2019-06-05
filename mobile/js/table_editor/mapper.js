Vue.component('com-table-mapper',{
    props:['head','row'],
    template:`<span class="com-table-mapper" v-text="label_text"></span>`,
    computed:{
        label_text(){
            var one = ex.findone(this.head.options,{value:this.row[this.head.name]})
            if(one){
                return one.label
            }else{
                return this.row[this.head.name]
            }

        }
    }
})