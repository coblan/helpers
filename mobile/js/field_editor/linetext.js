Vue.component('com-field-linetext',{
    props:['head','row'],
    template:`<van-field class="com-field-linetext" :class="{'readonly':head.readonly}"  v-model="row[head.name]" :required="head.required"
    :label="head.label"
    type="text"
    :placeholder="normed_placeholder"
    :name="head.name"
    autosize
    :error-message="head.error"
    :readonly="head.readonly"
    :maxlength="head.maxlength"
     :right-icon="head.help_text?'question-o':''"
    @click-right-icon="$toast(head.help_text)"
  >
  </van-field>`,
    mounted:function(){
        this.setup_validate_msg_router()
    },
    computed:{
        normed_placeholder:function(){
            if(! this.head.readonly){
                return this.head.placeholder || '请输入'+this.head.label
            }else{
                return ''
            }
        }
    },
    methods:{
        setup_validate_msg_router(){
            if(!this.head.validate_showError){
                Vue.set(this.head,'error','')
                this.head.validate_showError="scope.head.error=scope.msg"
            }
            if(!this.head.validate_clearError){
                this.head.validate_clearError="scope.head.error=''"
            }
        }
    }
})

