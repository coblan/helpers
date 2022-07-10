<template>
  <div class="editor-tab">



    <h2Drag save-name="_page_editor" :fixRight="true" style="width: 100%;background-color: transparent">
      <template v-slot:left>
<!--        <editorViewer :bus="bus"></editorViewer>-->
        <uie-mount-view :heads.sync="heads"></uie-mount-view>
      </template>
      <template v-slot:right>
        <editorTree :heads.sync="heads" @save="onSave"></editorTree>
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
        coms:[],
      },
      heads:JSON.parse(this.par_row.content)
    }
  },
  // computed:{
  //   heads(){
  //     return JSON.parse(this.par_row.content)
  //   }
  // },
  mounted(){
    this.bus.coms = JSON.parse(this.par_row.content)
  },
  methods:{
    async onSave(){
      this.par_row.content = JSON.stringify(this.heads)
      cfg.show_load()
      var resp = await ex.director_call('d.save_row',{row:this.par_row})
      cfg.hide_load()
      ex.vueAssign(this.par_row,resp.row)
      cfg.toast('保存成功')

    }
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