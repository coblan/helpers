<template>
  <div class="editor-tab">



    <h2Drag save-name="_page_editor" :fixRight="true" style="width: 100%">
      <template v-slot:left>
        <editorViewer :bus="bus"></editorViewer>
         <div style="flex-grow: 0">我是左边</div>
      </template>
      <template v-slot:right>
        <editorTree :bus="bus"></editorTree>
        <div>我是右边的</div>
      </template>
    </h2Drag>

<!--    <h3Drag></h3Drag>-->
  </div>
</template>
<script>
import editorViewer from './editorViewer.vue'
import editorTree from './editorTree.vue'
import  h2Drag from 'weblib/pc/layout/h2Drag.vue'
// import  h3Drag from 'weblib/pc/layout/h3Drag.vue'
export default {
  props:['tab_head','par_row'],
  components:{
    editorViewer,
    editorTree,
    h2Drag,
    // h3Drag
  },
  data(){
    return {
      bus:{
        coms:[]
      }
    }

  },
  mounted(){
    this.bus.coms = JSON.parse(this.par_row.content)
  }
}
</script>
<style scoped lang="scss">
.editor-tab{
  height: 100%;
  width: 100%;
  overflow: auto;
  display: flex;

}
</style>