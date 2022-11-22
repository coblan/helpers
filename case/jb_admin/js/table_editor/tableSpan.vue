<template>
  <span class="table-span">{{show_text}} </span>
<!--  @click="on_click()"-->
</template>
<script>
export default {
  props:['rowData','field','index'],
  computed:{
    show_text:function(){
      var value = this.rowData[this.field]
      if(this.head.hide_express){
        if(ex.eval(this.head.hide_express,{value:value})){
          return  ''
        }
      }
      if( value == undefined){
        return ''
      }else if(typeof value == 'object'){
        return JSON.stringify(value)
      } else{
        return this.rowData[this.field]
      }
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
    //     ex.eval(this.head.click_express,{row:this.rowData,head:this.head,ps:this.parStore})
    //   }
    // }
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
  //&:after{
  //  content:'...';
  //  font-weight:bold;
  //  position:absolute;
  //  bottom:0;
  //  right:0;
  //  padding:0 20px 1px 25px;
  //  background: white;
  //}
}
</style>
