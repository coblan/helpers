<template>
  <div class="login-page">
    <imageDiv class="bg" src="/static/authuser/image/login_bg.jpg"></imageDiv>
    <div class="login-form">
      <div class="big-head">
        {{tr('用户登录')}}
      </div>
      <div class="sub-title">
        <span class="sub-content">{{ctx.welcome || tr('欢迎登录后台管理系统')}}</span>
      </div>
      <loginForm></loginForm>

      <img src= '/static/authuser/image/login_shawdow.png' alt="" style="position: absolute;right: -30px;bottom: 0;width: 30px">
      <img src= '/static/authuser/image/login_shawdow.png' alt="" style="position: absolute;left: -30px;bottom: 0;width: 30px;transform: scaleX(-1)">

    </div>
  </div>
</template>
<script>
import imageDiv from 'weblib/uis/imageDiv.vue'
// import loginForm  from "webcase/pcweb/loginForm.vue";
import loginForm from "./loginForm.vue";
export  default  {
  components:{
    imageDiv,
    loginForm
  },
  props:{
    ctx:{}
  },
  methods:{
    tr(str){
      return cfg.tr(str)
    }
  }
}
</script>
<style scoped lang="scss">
.login-page{
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  .bg{
    position: absolute;
    top:0;
    left: 0;
    right: 0;
    bottom: 50%;
    z-index: -1;
  }
  .login-form{
    border: 1px solid #dcdcdc;
    background-color: white;
    position: relative;
    padding: 60px 30px 25px 30px;
    width: 380px;
    top:-66px;

    .big-head{
      //font-size: 160%;
      font-size: 30px;
      text-align: center;
      font-weight: 400;
    }
    .sub-title{
      text-align: center;
      margin: 10px auto;
      position: relative;
      background-color: white;
      height: 30px;
      &:before{
        content: '';
        display: block;
        left: 0;
        right: 0;
        height: 1px;
        background-color: #d9d9d9;
        top:50%;
        position: absolute;
      }
      .sub-content{
        position: absolute;
        white-space: nowrap;
        left: 50%;
        transform: translateX(-50%);
        background-color: white;
        top:4px;
        padding: 0 20px;
        font-size: 90%;
        color: black;
      }

    }

  }
}
</style>