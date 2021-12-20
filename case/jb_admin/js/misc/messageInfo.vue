<template>
  <div class="com-message-rows">
    <template  v-for='(row,index) in ctx.messages'>
      <span style="display: inline-block;padding: 0 10px">{{index+1}}:</span>
      <template v-if="row.type">
          <span :class="row.type">{{row.message}}</span>
      </template>
      <span v-else>{{row}}</span>
    </template>
  </div>
</template>
<script>
/*
* ctx: {messages}
* */
export default {
  props:{
    ctx:{}
  }
}
</script>
<style scoped lang="scss">
.com-message-rows{
  display: grid;
  grid-template-columns: auto 1fr;
}
.error{
  color: red;
}
</style>