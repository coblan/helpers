<template>
  <div class="table-tree-first" :class="head.class" style="display: inline-block">
    <component v-if="head.inn_editor"
               :is="head.inn_editor"
               :row-data="rowData" :field="field" :index="index"></component>
    <span v-else="" v-text="rowData[field]" ></span>
  </div>
</template>
<script>
export default {
  props:['rowData','field','index'],
  created:function(){
    // find head from parent table
    var table_par = this.$parent
    while (true){
      if (table_par.heads){
        break
      }
      table_par = table_par.$parent
      if(!table_par){
        break
      }
    }
    this.table_par = table_par
    this. head  = ex.findone(this.table_par.heads,{name:this.field})

    this.parStore = ex.vueParStore(this)
  },
}
</script>
<style lang="scss" scoped>
.table-tree-first:first-child{margin-left:23px}
.table-tree-first{
  vertical-align: bottom;
}
</style>