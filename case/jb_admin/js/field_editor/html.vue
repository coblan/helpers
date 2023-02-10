<template>
  <div class="com-field-html" v-html="row[head.name]">

  </div>
</template>
<script>
export default {
  props:['row','head'],
}
</script>
