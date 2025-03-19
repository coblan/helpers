<template>
  <div style="display: flex;position: absolute;left: 0;right: 0;bottom: 0;top:0;">
    <div style="width: 160px;padding: 10px;">
      <div style="padding: 10px 0;">
        <el-tag
            :key="row.pk"
            v-for="row in selected_rows"
            closable
            :disable-transitions="false"
            @close="handleClose(row)">
          {{row._label}}
        </el-tag>
      </div>
      <el-button v-if="selected_rows.length>0" type="success" size="mini" @click.native="finishSelect">确定选中项</el-button>
<!--      <div v-for="row in selected_rows">-->
<!--          {{row._label}}-->
<!--      </div>-->
    </div>
    <div style="flex-grow: 10">
      <com-backend-table :ctx="table_ctx" @finish="onFinish"></com-backend-table>
    </div>
  </div>

</template>
<script>
export default {
  props:{
    table_ctx:{}
  },
  data(){
    return {
      selected_rows:[]
    }
  },
  mounted(){
    debugger
  },
  methods:{
    onFinish(row){
      if(! ex.findone(this.selected_rows,{pk:row.pk})){
        this.selected_rows.push(row)
      }

    },
    handleClose(row){
      ex.remove(this.selected_rows,{pk:row.pk})
    },
    finishSelect(){
      this.$emit('finish',this.selected_rows)
    }
  }
}
</script>