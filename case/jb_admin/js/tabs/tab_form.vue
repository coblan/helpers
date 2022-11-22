<template>
  <div class="com-tab-fields-v1 com-tab-fields com-tab-form">
    <div v-if="show_front" class="front-message">
      <div class="message-content" v-html="tab_head.front_message"></div>
      <el-button @click="show_front=false" size="mini" type="primary">确定</el-button>
    </div>
    <com-form-one v-else :ctx="ctx"></com-form-one>
  </div>
</template>
<script>
export default {
  props:['tab_head','par_row'],
  data(){
    var ctx = this.tab_head.fields_ctx
    ex.assign(ctx,{
      par_row:this.par_row,
      init_express:this.tab_head.init_express,
    })
    if(this.tab_head.mounted_express){
      ctx.mounted_express = this.tab_head.mounted_express
    }
    return {
      childStore:{vc:this,name:'com-tab-form'},
      ctx:ctx,
      show_front:false,
    }
  },
  mounted(){
      if(this.tab_head.show_front_express){
        ex.eval(this.tab_head.show_front_express,{vc:this,par_row:this.par_row,head:this.tab_head})
      }
  }
}
</script>
<style scoped lang="scss">
.tab-full{
  // 只有在tab-full下，才是满屏窗口，需要在自身窗口里面滚动
  .com-tab-form{
    position: absolute;
    top:0;left:0;bottom: 0;right:0;overflow: auto;
  }
}
.front-message{
  width: 100%;
  text-align: center;
  padding-top: 20%;
  display: flex;
  justify-content: center;
  align-items: center;
  .message-content{
    font-size: 140%;
    display: inline-block;
    padding-right: 20px;
  }
}
</style>