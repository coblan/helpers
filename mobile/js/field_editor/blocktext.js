Vue.component('com-field-blocktext',{
    props:['head','row'],
    template:`<van-field class="com-field-linetext" v-model="row[head.name]" type="textarea" size="large"
    autosize
    clearable
    :label="head.label"
    :readonly="head.readonly"
    :placeholder="normed_placeholder"
    :name="head.name"
  ></van-field>`,
    computed:{
        normed_placeholder:function(){
            if(! this.head.readonly){
                return this.head.placeholder || '请输入'+this.head.label
            }else{
                return ''
            }
        }
    },
    mounted(){
        var org = this.row[this.head.name]
        this.row[this.head.name] +='.'
        setTimeout(()=>{
            this.row[this.head.name]= org
        },100)
    }
})