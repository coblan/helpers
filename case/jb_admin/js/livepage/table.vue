<template>
  <div class="live-table flex-grow">
    <com-backend-table v-if="tableCtx.autoHeight"  ref="btable" :ctx="tableCtx"></com-backend-table>
    <div class="wrap" v-else>
      <com-backend-table  ref="btable" :ctx="tableCtx"></com-backend-table>
    </div>

  </div>

</template>
<script>
export default {
  props:{
    tableCtx:{},
  },
}
</script>
<style scoped lang="scss">
.live-table{
  position: relative;
}
.wrap{
  position: absolute;
  top:0;
  left: 0;
  right: 0;
  bottom: 0;
}
</style>