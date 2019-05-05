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
                return this.head.placeholder || '请选择'+this.head.label
            }else{
                return ''
            }
        }
    }
})