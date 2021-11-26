<template>
  <div class="excel-process">
    <div class="success-input">成功导入<b>{{ctx.import_length}}</b>条</div>
    <div class="message">
      <div v-for="msg in ctx.messages">{{msg}}</div>
    </div>
  </div>
</template>
<script>
export  default  {
  props:{
    ctx:{}
  },

}
</script>
<style scoped lang="scss">
.excel-process{
  padding: 10px 20px;
}
.success-input{
  font-size:120%;
}

</style>
