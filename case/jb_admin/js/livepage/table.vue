<template>
  <com-backend-table  ref="btable" :ctx="tableCtx"></com-backend-table>
</template>
<script>
export default {
  props:{
    tableCtx:{},
  },
}
</script>