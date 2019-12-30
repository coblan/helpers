<template>
    <div class="live-login">
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
                        cfg.toast("登录成功");
                        setTimeout(function(){
                            location=window.search_args.next},1500)
                    }
                })
            }
        }
    }
</script>

<style scoped lang="scss">
.live-login{
    position: relative;
    height: var(--app-height);
    background: url("/static/mobile/UZuAHiafUi_small2.jpg");
    background-size: 100% 100%;
    color: #e1e1e1;
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
            display:inline-block;
            margin-left: .3rem;
            background-color: transparent;

            &::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
                color: #f7f7f7;
                opacity: 1; /* Firefox */
                font-style: italic;
            }
        }

    }
}
</style>