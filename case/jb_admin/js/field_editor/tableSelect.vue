<template>
  <div class="table-select">
<!--    <el-button size="mini">选择</el-button>-->
    <div style="display: inline-block;padding: 0 5px" v-for="row in selected_rows" :title="row.desp ||'' ">
      <el-tag size="small">{{row._label}}</el-tag>
    </div>

    <i class="el-icon-edit clickable" @click="openTable"></i>

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
   async mounted(){
    if(this.head.mounted_express){
      await ex.eval(this.head.mounted_express,{vc:this})
    }
    this.updateSelect()

  },
  computed:{
      out_value(){
        return this.row[this.head.name]
      }
  },
  watch:{
    out_value(){
      this.updateSelect()
    }
  },
  methods:{
    updateSelect(){
      if(this.head.format=='string'){ // 标识输出为字符串
        var list = ex.filter(this.row[this.head.name].split(',') ,item=>{return item!=''})
      }else{
        var list = this.row[this.head.name] || []
      }

      this.selected_rows = ex.map(list,item_id=>{
        var one= ex.findone(this.head.table_rows,{id:item_id})
        if(one){
          return  one
        }else{
          return {
            id:item_id,
            desp:item_id,
            _label:item_id,
          }
        }

      })
    },
     async openTable(){
      var rows = await cfg.pop_vue_com(popTable,{heads:this.head.table_heads,rows:this.head.table_rows,
        valid_values:this.head.valid_values,
        selected:this.selected_rows})
       this.selected_rows = rows
       if(this.head.format=='string'){
         this.row[this.head.name] = ex.map(this.selected_rows,item=>{ return item.id }).join(',')
       }else{
         this.row[this.head.name] = ex.map(this.selected_rows,item=>{ return item.id })
       }

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