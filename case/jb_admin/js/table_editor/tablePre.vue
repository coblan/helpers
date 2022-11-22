<template>
  <pre class="mypre">{{rowData[field]}}</pre>
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
<style scoped lang="scss">
.mypre{
  border: none;
  background: none;
  padding: 0;
}
</style>
