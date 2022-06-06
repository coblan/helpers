<template>
  <div class="flex">

    <div>
      <input type="text" v-model="keyword" placeholder="关键字">
      <com-backend-table  style="width: 450px"  ref="mytable" :ctx="tableCtx"></com-backend-table>
    </div>

    <div >
      <h3>{{current_row.com}}</h3>
      <div v-html="current_row.help_text"> </div>
    </div>
  </div>
</template>
<script>
export default {
    data(){
      var rows =[]
      for(var k in cfg.ui_editor){
        var com = cfg.ui_editor[k]
        rows.push({com:k,desp:com.desp,help_text:com.help_text})
      }
      return {
        current_row:{},
        rows:rows,
        tableCtx:{
          autoHeight:true,
          hasPagination:false,
          autoLoad:false,
          heads:[
            {name:'com',label:'组件',editor:'com-table-click',width:200,
              click_express:'scope.ps.vc.$emit("finish",scope.row)'},
            {name:'desp',label:'描述',width: 240,editor:'com-table-click',
              click_express:'scope.ps.vc.$emit("current_row",scope.row)'},

            // {name:'_op','label':'操作','editor':'com-table-ops-cell',
            //   'ops':[
            //     {'editor':'com-btn',
            //       'label':'选择',
            //       'type':'primary',
            //       'css':'.myphone button{ padding: 2px;}',
            //       'class':'myphone', click_express:'scope.ps.vc.parStore.vc.$emit("finish",scope.ps.vc.rowData)'}
            // ]}

          ],
          rows:rows,
          row_filters:[
            // {name:'com',label:'送',editor:'com-filter-text'}
          ],
          search_args:{},
          row_sort:{sortable:'',sort_str:''},
          row_pages:{},
          ops:[],
          selectable:false,
          option:{},
        },
        keyword:''
      }
    },
  mounted(){
      setTimeout(()=>{
        this.$refs.mytable.$refs.dtable.$on('current_row',this.onCurrentRow)
        this.$refs.mytable.$refs.dtable.$on('finish',this.onFinish)
      },1000)

  },
  watch:{
      keyword(){
          this.updateRows()
      }
  },
  methods:{
    updateRows(){
      if(this.keyword){
        var rows = ex.filter(this.rows,item=>{
          if(item.desp){
            return item.desp.indexOf(this.keyword) !=-1
          }
        })
        this.tableCtx.rows = rows

      }else {
        this.tableCtx.rows = this.rows
      }
    },
    onCurrentRow(row){
      this.current_row = row
    },
    onFinish(row){
      this.$emit('finish',row.com)
    }
  }
}
</script>