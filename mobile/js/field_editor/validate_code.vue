<template>
    <div class="com-field-validate-code" >
        <van-cell-group >
            <van-field
                    style="align-items: flex-start"
                    v-model="row[head.name]"
                    center
                    clearable
                    label="验证码"
                    placeholder="请输入验证码"
                    :data-mobile="row.mobile"
                    :name="head.name"
                    :error-message="head.error"
                    :required="head.required"
            >
                <!--<van-button slot="button" size="small" type="primary" @click.native="get_phone_code" :disabled="vcode_count!=0">-->
                    <!--<span v-text="vcodeLabel"></span>-->
                    <!--<img src="" alt="">-->
                <!--</van-button>-->
                <van-image slot="button"
                        width="2rem"
                        height="auto"
                        fit="contain"
                        :src="head.code_img"
                        @click="change_code"
                />
            </van-field>
        </van-cell-group>
    </div>
</template>
<script>
    export default{
        props:['head','row'],
        mounted(){
            this.setup_validate_msg_router()
        },
        methods:{
            change_code:function(){
                var self=this
                var post_data=[{fun:'new_validate_code'}]
                cfg.show_load()
                ex.post('/d/ajax/authuser',JSON.stringify(post_data),function(resp){
                    self.head.code_img=resp.new_validate_code
                    cfg.hide_load()
                })
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
    }
</script>