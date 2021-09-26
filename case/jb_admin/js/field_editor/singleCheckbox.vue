<template>
  <div class="com-field-single-checkbox">
    <el-checkbox v-model="row[head.name]"  :name="head.name" :disabled="head.readonly">
      {{head.check_label}}
    </el-checkbox>

  </div>
</template>
<script>
export default {
  props:['row','head'],
  mounted(){
    if(this.head.css){
      ex.append_css(this.head.css)
    }
  },
  computed:{
    my_label:function(){
      if(this.head.check_label){
        return this.head.check_label
      }else{
        return this.head.label
      }
    }
  }
}
</script>
<style scoped lang="scss">
.com-field-single-checkbox{
  position: relative;
  padding-top: 10px; // 感觉在field面板中 水平没对齐，所以往下挪动一下
}
</style>
