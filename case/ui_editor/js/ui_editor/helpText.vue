<template>
  <div>
    <h3>{{editor}}</h3>
    <div v-html="html_text"></div>
  </div>
</template>
<script>
export default {
  props:{

    editor:{}
  },
  computed:{
    html_text(){
      var com = cfg.ui_editor[this.editor]
      return com.help_text
    }
  }
}
</script>