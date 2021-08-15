<template>
  <batch_int class="com-table-batch-float" :row-data="rowData" :field="field" :index="index" :extend-logic="float_logic">

  </batch_int>

</template>

<script>
import batch_int  from "./batch_int.vue";

class FloatLogic{
  getSetup(props){
    var isNumber=function(evt){
      evt = (evt) ? evt : window.event;
      var charCode = (evt.which) ? evt.which : evt.keyCode;
//                if(charCode== 46){
//                    return evt.preventDefault();
//                }

      if ((charCode >= 48 && charCode <= 57) || charCode== 46 || charCode== 45) {
        var value = this.rowData[this.field]
        var value = String(value)
        if(charCode==46 && value.indexOf('.')!=-1){
          return evt.preventDefault();
        }else{
          return true
        }
      }else{
        return evt.preventDefault();
      }
    }
    return {
      isNumber
    }
  }
}

export default {
  props:['rowData','field','index'],
  components:{
    batch_int
  },
  data(){
    return {
      float_logic:FloatLogic,
    }
  },


  methods:{

  }
}
</script>

<!--<style scoped lang="scss">-->
<!--.my-input{-->
<!--  width: 100px;-->
<!--}-->
<!--</style>-->