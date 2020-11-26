Vue.component('com-field-linetext',{
    props:['head','row'],
    template:`<van-field class="com-field-linetext" :class="{'readonly':head.readonly}"  v-model="inn_data" :required="head.required"
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
    @blur="on_blur"
  >
  </van-field>`,
    mounted:function(){
        this.setup_validate_msg_router()
        if(this.head.mounted_express){
            ex.eval(this.head.mounted_express,{vc:this,row:this.row,head:this.head})
        }
    },
    data(){
        return {
            inn_data:this.row[this.head.name]
        }
    },
    watch:{
        outdata(nv){
            this.inn_data =nv
        }
    },
    computed:{
        outdata(){
            return this.row[this.head.name]
        },
        normed_placeholder:function(){
            if(! this.head.readonly){
                return this.head.placeholder || '请输入'+this.head.label
            }else{
                return ''
            }
        }
    },
    methods:{
        on_blur(e){
            Vue.set(this.row,this.head.name,this.inn_data)
            //this.row[this.head.name] = this.inn_data
        },
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

