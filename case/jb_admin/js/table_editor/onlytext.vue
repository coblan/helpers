<template>
  <span class="table-span" v-text="show_text" ></span>

</template>
<script>
export default {
  props:['rowData','field','index'],
  computed:{
    show_text:function(){
      return this.head.text
    }
  },
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
.table-span{
  display:inline-block;
  max-height: 50px;
}
</style>
