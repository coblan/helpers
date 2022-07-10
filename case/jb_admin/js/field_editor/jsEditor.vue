<template>
  <div class="editor">{{row[head.name]}}</div>
</template>
<script>
export default {
  props:['row','head'],
  mounted(){

    this. editor = ace.edit(this.$el);
    var JavaScriptMode = ace.require("ace/mode/javascript").Mode;
    this.editor.session.setMode(new JavaScriptMode());
    var par = ex.vueParStore(this)
    par.vc.before_submit.push(this.sumbitCode)
  },
  methods:{
    sumbitCode(){
      this.row[this.head.name] = this.editor.getValue()
    }
  }
}
</script>
<style lang="scss">
.editor {
  position: relative;
  width: 500px;
  height: 400px;
}
</style>