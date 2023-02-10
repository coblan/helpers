<template>
  <div :class="ctx.class" >
    <component v-for="com in ctx.com_list" :is="com.editor" v-bind="com" :ctx="com"></component>
  </div>
</template>

<script>
export default {
  name: "componentPannel.vue",
  props:{
    ctx:{

    }
  },
  mounted(){
    if(this.ctx.css){
      ex.append_css(this.ctx.css)
    }
  }
}
</script>

<style scoped>

</style>