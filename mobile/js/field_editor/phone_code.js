require('./styl/phone_code.styl')

Vue.component('com-field-phone-code',{
    /*
     parStore.get_phone_code(callback){

     }

     * */
    props:['row','head'],
    template:`<div class="com-field-phone-code" >
    <van-cell-group >
      <van-field
      style="align-items: flex-start"
        v-model="row[head.name]"
        center
        clearable
        label="短信验证码"
        placeholder="请输入短信验证码"
        :data-mobile="row.mobile"
        :name="head.name"
         :error-message="head.error"
         :required="head.required"
      >
    <van-button slot="button" size="small" type="primary" @click.native="get_phone_code" :disabled="vcode_count!=0">
        <span v-text="vcodeLabel"></span>
    </van-button>
    </van-field>
    </van-cell-group>
    </div>`,
    //template:` <div class="com-field-phone-code flex">
    //     <input  type="text" class="form-control input-sm" v-model="row[head.name]"
    //        :id="'id_'+head.name" :name="head.name"
    //        :placeholder="head.placeholder" :autofocus="head.autofocus" :maxlength='head.maxlength'>
    //
    //      <button type="button" class="btn btn-sm"
    //          :disabled="vcode_count !=0"
    //           @click="get_phone_code" v-text="vcodeLabel"></button>
    // </div>
    //`,
    data:function(){
        var parStore=ex.vueParStore(this)
        return {
            parStore:parStore,
            vcode_count:0
        }
    },
    computed:{
        vcodeLabel:function(){
            if(this.vcode_count != 0){
                return ''+this.vcode_count+' s'
            }else{
                return '获取验证码'
            }
        },
    },
    mounted(){
        this.setup_validate_msg_router()
    },
    methods:{
        get_phone_code:function(){
            var self=this

            if(! $(`input[name=${this.head.phone_field}]`).isValid() ){
                return
            }
            cfg.show_load()
            ex.eval(this.head.get_code,{row:this.row}).then((resp)=>{
                    cfg.hide_load()
                    self.vcode_count = self.head.vcode_count || 120
                    self.countGetVCodeAgain()
            })
            // 示例
            //ex.director_call('ali.phonecode',{mobile:this.vc.row.mobile}).then((resp)=>{
            //    cfg.hide_load()
            //    self.vcode_count = self.head.vcode_count || 120
            //    self.countGetVCodeAgain()
            //})

        },
        countGetVCodeAgain:function(){
            var self=this
            var idx = setInterval(function(){
                self.vcode_count -=1
                if(self.vcode_count<=0){
                    clearInterval(idx)
                    self.vcode_count=0
                }
            },1000)
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