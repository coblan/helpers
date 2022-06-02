<template>
  <div class="uie-mount-view">

    <template v-for="head in heads">
      <component v-if="head.children" :is="head.editor" :key="head.id"  v-bind="head.bind" :children="head.children"></component>
      <component v-else :is="head.editor" :key="head.id"  v-bind="head.bind"></component>
    </template>

  </div>
</template>
<script>
export default {
  props:{
    heads:{}
  },
  data(){
    return {

    }
  }
}
</script>