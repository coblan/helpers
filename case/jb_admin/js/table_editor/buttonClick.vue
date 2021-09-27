<template>
  <div class="button-click"  style="display: inline-block">
    <el-button type="goon" @click="on_click()" size="mini">{{head.button_label}}</el-button>
  </div>
</template>
<script>
export  default  {
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
.el-button--goon.is-active,
.el-button--goon:active {
  background: #20B2AA;
  border-color: #20B2AA;
  color: #fff;
}

.el-button--goon:focus,
.el-button--goon:hover {
  background: #48D1CC;
  border-color: #48D1CC;
  color: #fff;
}

.el-button--goon {
  color: #FFF;
  background-color: #20B2AA;
  border-color: #20B2AA;
}

</style>
