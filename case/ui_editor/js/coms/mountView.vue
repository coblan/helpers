<template>
  <div class="uie-mount-view">
    <component :is="head.editor" v-for="head in heads" v-bind="head.bind"></component>
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