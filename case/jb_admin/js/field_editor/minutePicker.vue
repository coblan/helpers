<template>
  <div  :class="['com-field-minute','field-'+head.name,head.class]" >
    <input v-if="!head.readonly" type="text" style="display: none"
           :id="'id_'+head.name"
           :name="head.name"
           v-model="row[head.name]">

    <el-time-picker
        v-model="row[head.name]"
        value-format="HH:mm"
        format="HH:mm"
        size="small"
        editable
        :placeholder="head.placeholder || '请输入时间'">
    </el-time-picker>
  </div>
</template>
<script>
export  default  {
  props:['row','head'],
  computed:{
    innvalue(){
      return this.row[this.head.name]
    }
  },
  watch:{
    innvalue(v){
      this.row[this.head.name] = v
      // debugger
      // if(v.length > 10){
      //   this.row[this.head.name] = v.slice(11)
      // }else{
      //   this.row[this.head.name] = v
      // }
    }
  },
  mounted(){
    if(this.head.css){
      ex.append_css(this.head.css)
    }
  },
}
</script>

<style scoped lang="scss">
.com-field-minute{
}

</style>
<!--<style lang="scss">-->
<!--.field-minute{-->
<!--  .el-time-spinner__wrapper:last-child{-->
<!--    display: none;-->
<!--  }-->
<!--}-->
<!--</style>-->