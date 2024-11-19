<template>
  <div>
    <el-form :model="row" :rules="rules" ref="ruleForm" label-width="0" class="real-form bootstrap-style">
      <el-form-item label="" prop="username">
        <el-input prefix-icon="el-icon-user" size="small" :placeholder="tr('用户名')" v-model="row.username"></el-input>
      </el-form-item>
      <el-form-item label="" prop="password" :error="arrayToStr(errors.password)">
        <el-input prefix-icon="el-icon-key"
                  @keydown.enter.native="submit"
                  type="password" size="small" :placeholder="tr('密码')" v-model="row.password"></el-input>
      </el-form-item>
      <el-form-item v-if="row.validate_img" label=""
                    :rules="{ required: true, message: tr('请输入验证码'), trigger: 'blur' }"
                    prop="validate_code" :error="arrayToStr(errors.validate_code)">
        <el-input class="validate-code" size="small" :placeholder="tr('验证码')" v-model="row.validate_code">
          <template slot="append" ><img :src="row.validate_img" alt=""></template>
        </el-input>
      </el-form-item>
      <el-checkbox v-model="row.auto_login"></el-checkbox> <span class="auto-log-text">{{tr('下次自动登录')}}</span>
    </el-form>

    <div class="dark-blue">
      <el-button  size="small" type="primary"  style="width: 100%" @click="submit()">{{tr('登录')}}</el-button>
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
          { required: true, message: cfg.tr('请输入用户名'), trigger: 'blur' },
        ],
        password:[
          { required: true, message: cfg.tr('请输入密码'), trigger: 'blur' },
        ],
        // validate_code:[
        //   { required: true, message: '请输入验证码', trigger: 'blur' },
        // ]
      },
      errors:{}
    }
  },
  computed:{
    mystyle(){
      return {
      }
    }
  },
  methods:{
    tr(str){
      return cfg.tr(str)
    },
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
.real-form{
  margin-bottom: 20px;
}
.auto-log-text{
  display: inline-block;
  margin-left: 3px;
  font-size: 90%;
}
.validate-code /deep/ .el-input-group__append{
  padding: 0;
  img{
    height: 25px;
    width: 100px;
  }
}
</style>