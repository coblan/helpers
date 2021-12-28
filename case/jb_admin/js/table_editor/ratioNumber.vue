<template>
  <span class="ratio-number" v-text="show_text"></span>
</template>
<script>
export default {
  props:['rowData','field','index'],
  computed:{
    show_text:function(){
      var value = this.rowData[this.field]
      if( value == undefined){
        return ''
      }
      var inn_value = parseFloat(value)
      var show_value =   inn_value * this.head.ratio
      return  show_value.toFixed(2)
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
  methods:{
    // on_click:function(){
    //   if(this.head.click_express){
    //     debugger
    //     ex.eval(this.head.click_express,{row:this.rowData,head:this.head,ps:this.parStore,vc:this})
    //   }
    // }
  }
}
</script>
<style scoped lang="scss">
.radio-number{
  display:inline-block;
  max-height: 50px;
}
</style>
