Vue.component('com-field-phone-code',{
    props:['row','head'],
    template:` <div  style="position: relative;" class="phone-code flex">
         <input  type="text" class="form-control input-sm" v-model="row[head.name]"
            :id="'id_'+head.name" :name="head.name"
            :placeholder="head.placeholder" :autofocus="head.autofocus" :maxlength='head.maxlength'>

          <button style="width: 9em" type="button" class="btn btn-default btn-sm"
              :disabled="vcode_count !=0"
               @click="sendGetCodeOrder()" v-text="vcodeLabel"></button>
     </div>
    `,
    data:function(){
        return {
            vcode_count:0
        }
    },
    computed:{
        vcodeLabel:function(){
            if(this.vcode_count!=0){
                return '获取验证码('+this.vcode_count+')'
            }else{
                return '获取验证码'
            }
        },
        hasValidPhone:function(){
            var mt =/^1[3-9]\d{9}$/.exec(this.row[this.head.phone_field])
            if(mt){return true}
            else {return false}
        },
    },
    methods:{
        sendGetCodeOrder:function(){
            var self=this
            if( !$(this.$parent.$el).find ('[name='+this.head.phone_field+']').isValid()){
                return
            }

            cfg.show_load()
            ex.director_call(this.head.fun,{row:this.row},function(resp){
                cfg.hide_load()

                setTimeout(function(){
                    self.countGetVCodeAgain()
                },1000)
            })

            //ex.vueParCall(this,'get_phone_code',{com_vcode:this})
            //this.$emit('field-event',{fun:'get_phone_code'})

        },
        //checkImageCode:function(phone,image_key,image_code){
        //    var self=this
        //    $(self.$el).find('input').trigger("hidemsg")
        //
        //    //if(this.row.image_code && this.hasValidPhone){
        //    var data={
        //        Phone:phone,
        //        Key:image_key,
        //        Answer:image_code,
        //    }
        //    cfg.show_load()
        //    service_post('/anonymity/vcode/generate',data,function(resp){
        //        if(resp.error_description){
        //            $(self.$el).find('input').trigger("showmsg", ["error", resp.error_description ])
        //        }else if(resp.success){
        //            //$(self.$el).find('.image_code').trigger("showmsg", ["ok", '正确' ])
        //            setTimeout(function(){
        //                //self.image_valid=true
        //                self.countGetVCodeAgain()
        //            },1000)
        //        }
        //        // else {
        //        //    $(self.$el).find('.image_code').trigger("showmsg", ["error", resp.error_description ])
        //        //}
        //
        //    },false)
        //    //}
        //},
        countGetVCodeAgain:function(){
            var self=this
            self.vcode_count=120
            var idx = setInterval(function(){
                self.vcode_count -=1
                if(self.vcode_count<=0){
                    clearInterval(idx)
                    self.vcode_count=0
                }
            },1000)
        },
    }
})