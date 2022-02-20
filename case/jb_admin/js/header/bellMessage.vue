<template>
  <li class="bell-message" @click="on_click()">
    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
      <i class="fa fa-bell-o"></i>
      <span v-if="ctx.count !=0 " class="label label-warning" v-text="ctx.count"></span>
    </a>
  </li>
</template>
<script>
export default {
  props:['ctx'],
  methods:{
    on_click:function(){
      if(this.ctx.click_express){
        ex.eval(this.ctx.click_express)
      }
    }
  }
}
</script>
<style scoped lang="scss">
.bell-message{
  float: left;
}
</style>