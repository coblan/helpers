<template>
  <div class="pop-table-select">
    <simTable :heads="heads" :rows="rows" :selected="inn_selected" :showSelect="true" @changed="onChange" :valid_values="valid_values"></simTable>
    <div style="padding: 20px;margin-top: 20px">
      <el-button size="mini" type="primary" @click="makesure">确定选择</el-button>
    </div>

  </div>
</template>
<script>
import simTable from 'webcase/pcweb/uis/simTable.vue'
export  default  {
  components:{
    simTable
  },
  props:{
    heads:{},
    rows:{},
    selected:{},
    valid_values:{}
  },
  data(){
    return {
      mydata:[],
      inn_selected:ex.copy(this.selected)
    }
  },
  methods:{
    onChange(e){
      this.mydata = e
    },
    makesure(){
      this.$emit('finish',this.mydata )
    }
  }
}
</script>

<style scoped lang="scss">
.pop-table-select{
  padding: 20px;

}
</style>