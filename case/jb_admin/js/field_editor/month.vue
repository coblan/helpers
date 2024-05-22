<template>
  <div class="com-field-month" :style="{'--width':this.head.width}">
    <input style="display: none" type="text"
           :id="'id_'+head.name" v-model="row[head.name]"
           :name="head.name">
    <el-date-picker
        v-model="row[head.name]"
        type="month"
        :readonly="head.readonly"
        size="small"
        value-format="yyyy-MM"
        :placeholder="head.placeholder || '选择月份'">
    </el-date-picker>

  </div>
</template>
<script>
export default {
  props:['row','head'],
  template:``,
  mounted:function(){
  }
}
</script>
<style scoped lang="scss">
.com-field-month{
  ::v-deep{
    .el-date-editor.el-input{
      width: var(--width);
    }
    input{
      width: var(--width);
    }
  }
}
</style>


