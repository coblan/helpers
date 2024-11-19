<template>
  <li class="dropdown messages-menu">

    <el-dropdown  trigger="click">
        <div class="el-dropdown-link my-drop-down">
          {{ctx.label}}<i class="el-icon-arrow-down el-icon--right"></i>
        </div>

        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item v-for="action in ctx.options" @click.native="runAction(action)">{{action.label}}</el-dropdown-item>
        </el-dropdown-menu>
    </el-dropdown>



  </li>
</template>
<script>
export  default  {
  props:['ctx'],
  methods:{
    runAction(action){
      ex.eval(action.click_express)
    }
  }
}
</script>
<style scoped lang="scss">
.my-drop-down{
  color: white;
  //padding-top: 15px;
  //padding-bottom: 15px;
  line-height: 20px;
  padding: 15px;

  &:hover{
    background: rgba(0, 0, 0, 0.1);
    color: #f6f6f6;
  }
}
</style>