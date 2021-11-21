<template>
  <div class="login-page" :style="mystyle">
    <imageDiv class="bg" src="/static/authuser/image/login_bg.jpg"></imageDiv>
    <div class="login-form">
      <div class="big-head">
        用户登录
      </div>
      <div class="sub-title">
        <span class="sub-content">欢迎登录后台管理系统</span>

      </div>
      <el-form :model="row" :rules="rules" ref="ruleForm" label-width="0" class="demo-ruleForm">
        <el-form-item label="" prop="username">
          <el-input prefix-icon="el-icon-user" size="small" placeholder="用户名" v-model="row.username"></el-input>
        </el-form-item>
        <el-form-item label="" prop="name" error="jjyy">
          <el-input prefix-icon="el-icon-key" size="small" placeholder="密码" v-model="row.name"></el-input>
        </el-form-item>
      </el-form>
      <el-button size="small" type="primary" style="width: 100%" @click="submit">提交</el-button>
      <img src= '/static/authuser/image/login_shawdow.png' alt="" style="position: absolute;right: -30px;bottom: 0;width: 30px">
      <img src= '/static/authuser/image/login_shawdow.png' alt="" style="position: absolute;left: -30px;bottom: 0;width: 30px;transform: scaleX(-1)">

    </div>
  </div>
</template>
<script>
import imageDiv from 'weblib/uis/imageDiv.vue'
export  default  {
  components:{
    imageDiv,
  },
  props:{
    ctx:{}
  },
  data(){
    return {
      row:{
        username:'',
        password:'',
        validate_img:'',
        auto_login:true,
      },
      rules:{
        username:[
          { required: true, message: '请输入用户名', trigger: 'blur' },
        ]
      }
      // background:this.ctx.background || '/static/authuser/image/login_bg.jpg'
    }
  },
  computed:{
    mystyle(){
      return {
      }
    }
  },
  methods:{
    async submit(){
      var post_data ={
        row:this.row
      }
      cfg.show_load()
      var resp = await  ex.director_call('do_login',post_data)
      cfg.hide_load()
      debugger
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
    padding: 60px 30px 20px 30px;
    width: 300px;
    top:-50px;
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