<template>
  <div class="table-select">
    <!--    <el-button size="mini">选择</el-button>-->
<!--    <div style="display: inline-block;padding: 0 5px" v-for="row in selected_rows" :title="row.desp">-->
<!--      <el-tag size="small">{{row._label}}</el-tag>-->
<!--    </div>-->
    <span>{{out_value}}</span>

<!--    <span style="padding: 0 10px">-->
      <el-button type="primary" size="mini" icon="el-icon-edit" @click.native="openTable"></el-button>
<!--         <i class="el-icon-edit clickable"  @click="openTable"></i>-->
<!--    </span>-->

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
    if(this.head.mounted_express){
      ex.eval(this.head.mounted_express,{vc:this,})
    }
  },
  computed:{
    out_value(){
      return this.row[this.head.name]
    }
  },
  // watch:{
    // out_value(){
      // this.updateSelect()
    // }
  // },
  methods:{
    // updateSelect(){
    //   var list = this.row[this.head.name] || []
    //   this.selected_rows = ex.map(list,item_id=>{
    //     var one= ex.findone(this.head.table_rows,{id:item_id})
    //     return one
    //   })
    // },
    async openTable(){
      if(this.head.click_express){
        ex.eval(this.head.click_express,{vc:this,head:this.head})
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
  //flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  min-height: 32px;
  border: 1px solid #eeeded;
  border-radius: 3px;
  row-gap: 10px;
}
</style>