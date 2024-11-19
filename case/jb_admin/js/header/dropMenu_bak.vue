<template>
  <li class="dropdown messages-menu">
    <!-- Menu toggle button -->
    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
      <!--      <i class="fa fa-envelope-o"></i>-->
      <!--      <span class="label label-success">4</span>-->
      <i class="fa fa-user-circle-o"></i>
      <span>{{ctx.label}}</span>
    </a>
    <ul class="dropdown-menu">
      <li class="my-row" v-for="action in ctx.options" @click="runAction(action)">{{action.label}}</li>

      <!--      <li>-->
      <!--&lt;!&ndash;         inner menu: contains the messages &ndash;&gt;-->
      <!--        <ul class="menu">-->

      <!--          &lt;!&ndash; end message &ndash;&gt;-->
      <!--        </ul>-->
      <!--        &lt;!&ndash; /.menu &ndash;&gt;-->


      <!--      </li>-->

    </ul>
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
</style>