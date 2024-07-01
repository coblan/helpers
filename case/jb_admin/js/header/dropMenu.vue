<template>
  <li class="dropdown messages-menu">

    <el-dropdown  trigger="click">
        <div class="el-dropdown-link my-drop-down">
          {{ctx.label}}<i class="el-icon-arrow-down el-icon--right"></i>
        </div>
<!--      <a href="#" class="dropdown-toggle" data-toggle="dropdown">-->
<!--        &lt;!&ndash;      <i class="fa fa-envelope-o"></i>&ndash;&gt;-->
<!--        &lt;!&ndash;      <span class="label label-success">4</span>&ndash;&gt;-->
<!--        <i class="fa fa-user-circle-o"></i>-->
<!--        <span>{{ctx.label}}</span>-->
<!--      </a>-->

        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item v-for="action in ctx.options" @click="runAction(action)">{{action.label}}</el-dropdown-item>
        </el-dropdown-menu>
    </el-dropdown>


    <!-- Menu toggle button -->
<!--    <a href="#" class="dropdown-toggle" data-toggle="dropdown">-->
<!--&lt;!&ndash;      <i class="fa fa-envelope-o"></i>&ndash;&gt;-->
<!--&lt;!&ndash;      <span class="label label-success">4</span>&ndash;&gt;-->
<!--      <i class="fa fa-user-circle-o"></i>-->
<!--      <span>{{ctx.label}}</span>-->
<!--    </a>-->
<!--    <ul class="dropdown-menu">-->
<!--      <li class="my-row" v-for="action in ctx.options" @click="runAction(action)">{{action.label}}</li>-->

<!--    </ul>-->
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
.dropdown-menu{
  width: auto !important;
  border:1px solid #ebeef5;
  padding: 5px 0 !important;
  min-width: 100px;
}
.my-row{
  padding: 8px 20px;
  background-color: white;
  &:hover{
    background-color: #ecf5ff;
    color: #66b1ff;
    cursor: pointer;
  }
}
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