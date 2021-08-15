<template>
  <div v-html="ctx.html">
  </div>
</template>
<script>
export default {
  props: ['ctx'],
}
</script>