Vue.component('com-field-pop-table-select',{
    props:['head','row'],
    template:`<van-field class="com-field-pop-table-select"  v-model="row[head.name]" :required="head.required"
    :label="head.label"
    type="text"
    :placeholder="normed_placeholder"
    :name="head.name"
    autosize
    :error-message="head.error"
    @click="open_win"
    readonly
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
        open_win(){
            cfg.pop_big('com-field-pop-search',{table_ctx:this.head.table_ctx,placeholder:this.head.search_placeholder})
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


Vue.component('com-field-pop-search',{
    props:['ctx'],
    template:`<div class="com-field-pop-search">
    <van-search
    v-model="value"
    :placeholder="this.ctx.placeholder || '请输入搜索关键词'"
    show-action
    @search="onSearch"
    @cancel="onCancel"
  />
  <com-ctn-scroll-table :ctx="ctx"> </com-ctn-scroll-table>

    </div>`,
    data(){
        return {
            value:''
        }
    },
    methods:{
        onSearch(){

        },
        onCancel(){
            history.back()
        }
    }
})
