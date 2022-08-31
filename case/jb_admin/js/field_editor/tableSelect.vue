<template>
  <div class="table-select">
<!--    <el-button size="mini">选择</el-button>-->
    <div style="display: inline-block;padding: 0 5px" v-for="row in selected_rows" :title="row.desp">
      <el-tag size="small">{{row._label}}</el-tag>
    </div>

    <i class="el-icon-edit clickable" @click="openTable"></i>

<!--    <simTable v-if="selected_rows.length>0" :heads="head.table_heads" :rows="selected_rows" :showHead="true"></simTable>-->
  </div>
</template>
<script>
import popTable from "./tableSelect/popTable.vue";
import simTable from 'webcase/pcweb/uis/simTable.vue'
export default {
  components:{
    simTable
  },
  props:['row','head'],
  data(){
    return {
      selected_rows:[]
    }
  },
  mounted(){
    var list = this.row[this.head.name] || []
    this.selected_rows = ex.map(list,item_id=>{
      var one= ex.findone(this.head.table_rows,{id:item_id})
      return one
    })
  },
  methods:{
     async openTable(){
      var rows = await cfg.pop_vue_com(popTable,{heads:this.head.table_heads,rows:this.head.table_rows,selected:this.selected_rows})
       this.selected_rows = rows
       this.row[this.head.name] = ex.map(this.selected_rows,item=>{ return item.id })
    }
  }

}
</script>
<style scoped lang="scss">
.table-select{
  background-color: white;
  width: 23rem;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  min-height: 32px;
  border: 1px solid #eeeded;
  border-radius: 3px;
  row-gap: 10px;
}
</style>