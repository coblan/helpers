<template>
    <div class="live-login"
         :style="{backgroundImage:'url(/static/mobile/76f93439-7072-45dd-b257-c09603e01ad7_thumb.jpg)'}">
        <div class="login-form">
            <div class="title">
                <span v-html="ctx.title"></span>
            </div>
            <div class="row">
                <van-icon name="user-o"  />
                <input type="text" v-model="username" placeholder="请输入账号">
            </div>
            <div class="row">
                <van-icon name="lock"  />
                <input type="password" v-model="password" placeholder="请输入密码">
            </div>

            <div style="padding-top: .3rem">
                <van-button type="primary" size="large" @click="do_login">登录</van-button>
            </div>

        </div>
        <div class="footer" v-if="ctx.footer">
            <template v-for="(item,index) in ctx.footer">
                <div v-text="item.label" @click="on_click(item)"></div>
                <div v-if="index != (ctx.footer.length -1)"  class="spliter"></div>
            </template>
            <!--<div>忘记密码</div>-->
            <!--<div class="spliter"></div>-->
            <!--<div>立即注册</div>-->
        </div>
    </div>
</template>
<script>
    export default {
        props:['ctx'],
        basename:'live_login',
        data(){
            return {
                username:'',
                password:'',

            }
        },
        methods:{
            do_login(){
                var post_row = { username:this.username,password:this.password,_director_name:this.ctx.director_name }
                cfg.show_load()
                ex.director_call('d.save_row',{row:post_row }).then((resp)=>{
                    cfg.hide_load()
                    if(resp.errors){
                        for(var k in resp.errors){
                            cfg.toast(resp.errors[k][0])
                            break
                        }
                    }else{
                        ex.eval(this.ctx.after_save)
//                        cfg.toast("登录成功");
//                        setTimeout(function(){
//                            location=window.search_args.next},1500)
                    }
                })
            },
            on_click(item){
                ex.eval(item.action)
            }
        }
    }
</script>

<style scoped lang="scss">
.live-login{
    position: relative;
    height: var(--app-height);
    background-size: 100% 100%;
    color: white;
    /*background-image: url('@/static/mobile/76f93439-7072-45dd-b257-c09603e01ad7_thumb.jpg');*/

}
.login-form{
    width: 70%;
    position: absolute;
    top:50%;
    left: 50%;
    transform: translate(-50%,-50%);
    .title{
        font-size: .4rem;
        /*color: #3a3a3a;*/
        font-weight: 500;
        letter-spacing: .2rem;
        /*font-style: italic;*/
        text-align: center;
        position: relative;
        top:-.5rem;
    }
    .row{
        display: flex;
        padding: .3rem;
        border-bottom: 1px solid #d5d5d5;
        margin: .3rem 0;
        font-size:.32rem;
        input{
            /*color: #665656;*/
            display:inline-block;
            margin-left: .3rem;
            background-color: transparent;

            &::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
                color: #9f9a9c;
                opacity: 1; /* Firefox */
                /*font-style: italic;*/
                font-size: .26rem;
            }
        }

    }
}

.footer{
    background-color: rgba(6,6,6,.2);
    position: absolute;
    bottom: 0;
    height: .8rem;
    display: flex;
    width: 100%;
    justify-content:space-around;
    align-items:center;
    /*div.item{*/
        /*position:relative;*/
        /*&::after{*/
             /*content: '';*/
             /*display: block;*/
             /*height: .3rem;*/
             /*background-color: white;*/
             /*width: 1px;*/
             /*position: absolute;*/
            /*right: -.4rem;*/
             /*top: -.1rem;*/
         /*}*/
    /*}*/
    .spliter{
        position: absolute;
        left: 50%;
        width: 1px;
        height: .3rem;
        background-color: white;
    }
}
</style>