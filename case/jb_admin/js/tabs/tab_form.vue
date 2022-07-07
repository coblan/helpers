<template>
  <div class="com-tab-fields-v1 com-tab-fields com-tab-form">
    <com-form-one :ctx="ctx"></com-form-one>
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
      mounted_express:this.tab_head.mounted_express,
    })
    return {
      ctx:ctx
    }
  },
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

</style>