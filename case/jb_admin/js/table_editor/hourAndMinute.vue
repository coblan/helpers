<template>
  <div class="table-hour-and-minute"  style="display: inline-block">
    <span>{{hour}}</span>: <span>{{minute}}</span>
  </div>
</template>
<script>

function padNumber(num, fill) {
  //改自：http://blog.csdn.net/aimingoo/article/details/4492592
  var len = ('' + num).length;
  return (Array(
      fill > len ? fill - len + 1 || 0 : 0
  ).join(0) + num);
}

export  default  {
  props:['rowData','field','index'],
  computed:{
    hour(){
      var vv = this.rowData[this.field]
      if(vv){
        return padNumber( parseInt( parseInt(vv) /60 ),2  )
      }else{
        return  0
      }
    },
    minute(){
      var vv = this.rowData[this.field]
      if(vv){
        return padNumber(  parseInt(vv) % 60 ,2 )
      }else{
        return  0
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

}
</script>
<style scoped lang="scss">


</style>
