<template>
  <div>
    <el-button size="mini" type="primary" @click="onClick">选择</el-button>
  </div>
</template>
<script>
import comTable from "./comTable.vue";
export default {
  methods:{
    onClick(){
      cfg.pop_vue_com(comTable,{})
    }
  }
}
</script>