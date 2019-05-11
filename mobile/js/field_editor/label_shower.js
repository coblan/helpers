Vue.component('com-field-label-shower',{
    props:['head','row'],
    template:`<van-field class="com-field-label-shower"
    v-model="label_text"
    :label="head.label"
    type="text"
    :name="head.name"
    autosize
    readonly
  >
  </van-field>`,
    computed:{
        label_text(){
            return this.row['_'+this.head.name+'_label']
        }
    },
})

