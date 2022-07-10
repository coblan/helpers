<template>
  <div>
    <span style="display: inline-block;margin-right: 10px">{{myvalue}}</span>
    <el-button size="mini" type="primary" @click="onClick">选择</el-button>
  </div>
</template>
<script>
import comTable from "./comTable.vue";
export default {
  props:['row','head'],
  methods:{
    async onClick(){
      var resp = await cfg.pop_vue_com(comTable,{})
      this.$set(this.row,this.head.name,resp)
      // this.row[this.head.name] = resp
    }
  },
  computed:{
    myvalue(){
      return this.row[this.head.name]
    }
  }

}
</script>