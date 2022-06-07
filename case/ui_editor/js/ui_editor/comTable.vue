<template>
  <div class="flex">

    <div>
      <div class="flex">
        <com-field-linetext :head="{name:'free_word',}" :row="word_row"></com-field-linetext>
<!--        <input type="text" v-model="keyword" placeholder="关键字">-->
        <com-field-select :head="{name:'first_word',options:firstkey_options}" :row="word_row"></com-field-select>
      </div>

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
        firstkey_options:[
          {value:'Echarts',label:'Echarts'}
        ],
        word_row:{},

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
        // keyword:''
      }
    },
  mounted(){
      setTimeout(()=>{
        this.$refs.mytable.$refs.dtable.$on('current_row',this.onCurrentRow)
        this.$refs.mytable.$refs.dtable.$on('finish',this.onFinish)
      },1000)

  },
  computed:{
      keyword(){
        var regword = ''
        if(this.word_row.free_word){
          regword += this.word_row.free_word
        }
        if(this.word_row.first_word){
          regword += this.word_row.first_word
        }
        return regword
      }
  },
  watch:{
      keyword(){
          this.updateRows()
      }
  },
  methods:{
    updateRows(){
      if(this.keyword){
        var r1=null
        var r2 = null
        if(this.word_row.free_word){
          var word_ls = ex.filter(this.word_row.free_word.split(' '),item=>{ return item !=''} )
          if(word_ls.length >0) {
            var regword = word_ls.join('|')
            r1 = RegExp(regword,"i");
          }
        }
        if(this.word_row.first_word){
          r2 = RegExp(this.word_row.first_word,"i");
        }

        var rows = ex.filter(this.rows,item=>{
          if(item.desp){
            var rt = true
            if(r1){
              rt = rt && r1.test(item.desp)
            }
            if(r2){
              rt = rt && r2.test(item.desp)
            }
            return rt
            // return item.desp.indexOf(this.keyword) !=-1
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