<template>
  <div class="com-field-date" :style="mysytle">
    <span class="readonly-info" v-show='head.readonly' v-text='row[head.name]'></span>

    <input v-if="!head.readonly" type="text" style="display: none"
           :id="'id_'+head.name"
           :name="head.name"
           v-model="row[head.name]">
    <el-date-picker
        v-if="!head.readonly"
        v-model="row[head.name]"
        type="date"
        :placeholder="head.placeholder"
        align="right"
        size="small"
        value-format="yyyy-MM-dd"
        :picker-options="pickerOptions">
    </el-date-picker>
  </div>
</template>
<script>
export default {
  props:['row','head'],
  data(){
    return {
      pickerOptions: {
        shortcuts: [{
          text: '今天',
          onClick(picker) {
            var d = new Date();
            d.setHours(0,0,0,0);
            picker.$emit('pick', d);
          }
        }, {
          text: '昨天',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24);
            date.setHours(0,0,0,0);
            picker.$emit('pick', date);
          }
        }, {
          text: '一周前',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
            date.setHours(0,0,0,0);
            picker.$emit('pick', date);
          }
        },{
          text: '30天前',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 30);
            date.setHours(0,0,0,0);
            picker.$emit('pick', date);
          }
        }]
      },
    }
  },
  computed:{
    mysytle(){
      return {
        '--width':this.head.width || 'auto',
        '--input_width':this.head.width || '23rem',
      }
    },
  }
}
</script>

<style scoped lang="scss">

// .field_input.input是23rem，element.date组件写死了input外层div只有220px宽度，比input的小很多。造成nicevalidator的错误消息显示在input内部。
// 本来在 field_input 的css里面有控制这个宽度，但是date组件在外部单独使用时，就没css控制了。所以在这里单独进行控制，适应性更广。
.com-field-date{
  /deep/{
    .el-date-editor.el-input, .el-date-editor.el-input__inner{
      width: var(--width) !important;
    }
    .el-date-editor input{
      width: var(--input_width);
    }
  }
}
</style>
