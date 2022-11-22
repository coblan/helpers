<template>
  <div class="com-table-click clickable" :class="head.class" @click="on_click()" style="display: inline-block">
    <component v-if="head.inn_editor"
               :is="head.inn_editor"
               :row-data="rowData" :field="field" :index="index"></component>
    <span class="table-span"  v-else v-text="rowData[field]" ></span>
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
  methods:{
    on_click:function(){
      var click_express= this.head.click_express || this.head.action

      ex.eval(click_express,{row:this.rowData,head:this.head,ps:this.parStore,vc:this})
      //this.$emit('on-custom-comp',{name:this.head.fun,row:this.rowData,head:this.head})
    }
  }
}
</script>
<style scoped lang="scss">
.table-span{
  display:inline-block;
//max-height: 500px;
  position: relative;
  overflow:hidden;

  overflow:hidden;
  text-overflow:ellipsis;
  display:-webkit-box;
  -webkit-line-clamp:5;
  -webkit-box-orient:vertical;
}
</style>