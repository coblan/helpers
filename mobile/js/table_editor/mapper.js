Vue.component('com-table-mapper',{
    props:['head','row'],
    template:`<div class="com-table-mapper" :class="cssclass" v-text="label_text"></div>`,
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
    },
    computed:{
        label_text(){
            var one = ex.findone(this.head.options,{value:this.row[this.head.name]})
            if(one){
                return one.label
            }else{
                return this.row[this.head.name]
            }

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