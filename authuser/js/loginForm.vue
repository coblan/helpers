<template>
  <div class="login-page" :style="mystyle">
    <imageDiv class="bg" src="/static/authuser/image/login_bg.jpg"></imageDiv>
    <div class="login-form bootstrap-style">
      <div class="big-head">
        用户登录
      </div>
      <div class="sub-title">
        <span class="sub-content">欢迎登录后台管理系统</span>
      </div>
      <el-form :model="row" :rules="rules" ref="ruleForm" label-width="0" class="real-form">
        <el-form-item label="" prop="username">
          <el-input prefix-icon="el-icon-user" size="small" placeholder="用户名" v-model="row.username"></el-input>
        </el-form-item>
        <el-form-item label="" prop="password" :error="arrayToStr(errors.password)">
          <el-input prefix-icon="el-icon-key" type="password" size="small" placeholder="密码" v-model="row.password"></el-input>
        </el-form-item>
        <el-form-item v-if="row.validate_img" label=""
                      :rules="{ required: true, message: '请输入验证码', trigger: 'blur' }"
                      prop="validate_code" :error="arrayToStr(errors.validate_code)">
          <el-input class="validate-code" size="small" placeholder="验证码" v-model="row.validate_code">
            <template slot="append" ><img :src="row.validate_img" alt=""></template>
          </el-input>
        </el-form-item>
        <el-checkbox v-model="row.auto_login"></el-checkbox> <span class="auto-log-text">下次自动登录</span>
      </el-form>

      <div class="dark-blue">
        <el-button  size="small" type="primary"  style="width: 100%" @click="submit()">登录</el-button>
      </div>


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
        ],
        password:[
          { required: true, message: '请输入密码', trigger: 'blur' },
        ],
        // validate_code:[
        //   { required: true, message: '请输入验证码', trigger: 'blur' },
        // ]
      },
      errors:{}
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
    arrayToStr(array){
      if(array && array.length >0){
        return array.join(';')
      }else{
        return  ''
      }
    },
    async submit(){
      var resp  =await   this.$refs.ruleForm.validate()
      this.errors={}

      var post_data ={
        row:this.row
      }
      cfg.show_load()
      var resp = await  ex.director_call('do_login',post_data)
      cfg.hide_load()
      var success = true
      if(resp.validate_img){
        this.row.validate_img= resp.validate_img
        success = false
      }
      if(resp.errors){
        ex.vueAssign(this.errors,resp.errors)
        success = false
      }
      if(success){
        var search = ex.parseSearch()
        location = search.next || '/'
      }
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
    width: 300px;
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
    .real-form{
      margin-bottom: 20px;
    }
    .auto-log-text{
      display: inline-block;
      margin-left: 3px;
      font-size: 90%;

    }
  }
}
.validate-code /deep/ .el-input-group__append{
  padding: 0;
  img{
    height: 25px;
    width: 100px;
  }
}
</style>