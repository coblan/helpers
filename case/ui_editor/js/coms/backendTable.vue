<template>

    <com-backend-table v-if="loaded"  ref="btable" :ctx="tableCtx" class="uie-backend-table"></com-backend-table>

</template>
<script>
import  ex from 'weblib/ex'
export default {
  props:{
    director_name:{}
  },
  data(){
    return {
      tableCtx: {},
      loaded:false,
    }
  },
  mounted(){
      this.getData()
  },
  methods:{
    async getData(){
      var resp = await ex.director_get("d.get_context",{director_name: this.director_name} )
      resp.autoHeight=true
      resp.opMergeCount =4
      this.tableCtx = resp
      this.loaded = true
    }
  }
}

cfg.ui_editor['uie-backendTable'] = {
  fields:[
    {name:'director_name',label:'director name',editor:'com-field-linetext',help_text: '直接填写后台table的director_name即可'},
  ],
  desp:'后台table',
  help_text:`<div>直接填写后台table的director_name即可</div>`
}
</script>
<style scoped lang="scss">
.uie-backend-table{
  background-color: white;
}
</style>