<template>
  <div class="com-table-multi-row">
    <div class="myrow" v-for="(row,rindex) in rows" >
      <component :is="head.row_editor" :rowData="row" :field="head.name" :index="rindex"></component>
    </div>
  </div>
</template>

<script>
export default {
  props:['rowData','field','index'],
  data(){
    this.init_head()
    return {
      parStore:ex.vueParStore(this)
    }
  },

  mounted(){
    // 如果整行的高度不是由 本插件撑起来的时候，改列内容会跑到中间，看起来比较怪异，所以设置 顶部对齐
    $(this.$el).parent().parent().css("vertical-align", "top")
    setTimeout(()=>{
      this.update_title()
    },1000)
    this.parStore.$on('header-dragend',this.on_drag)
  },
  computed:{
    rows(){
      if(! Boolean(this.rowData[this.head.rows_field])){
        return []
      }
      if( typeof this.rowData[this.head.rows_field] =='string'){
        var rows = JSON.parse(this.rowData[this.head.rows_field])
      }else{
        var rows = this.rowData[this.head.rows_field]
      }
      return rows
    },
    mydata(){
      //debugger
      //if( typeof this.rowData[this.head.rows_field] =='string'){
      //    var rows = JSON.parse(this.rowData[this.head.rows_field])
      //}else{
      //    var rows = this.rowData[this.head.rows_field]
      //}
      var rows =  this.rows ;//this.rowData[this.head.rows_field]

      return  ex.map(rows,(row)=>{return row[this.field]})
    }
  },
  watch:{
    mydata(){
      setTimeout(()=>{
        this.update_title()
      },1000)
    }
  },
  methods:{
    init_head(){
      var table_par = this.$parent
      while (true){
        if (table_par.heads){
          break
        }
        table_par = table_par.$parent
        if(!table_par){
          break
        }
      }
      this.table_par = table_par
      this.head = ex.findone(this.table_par.heads,{name:this.field})
    },
    on_drag(kws){
      //newWidth, oldWidth, column, event
      if(kws.column.property == this.field){
        setTimeout(()=>{
          this.update_title()
        },1000)
      }
    },
    update_title(){

      ex.each($(this.$el).find('.myrow'),mydiv=>{
        if( $(mydiv).width() <  $(mydiv).find('span').width() ){
          $(mydiv).attr('title',mydiv.textContent)
        }else{
          $(mydiv).attr('title','')
        }
      })
    },

  }
}
</script>
<style scoped lang="scss">
.com-table-multi-row{
  padding-top: 2px;
  .myrow:not(:last-child):after{
    content: '';
    display: block;
    width: 100%;
    height: 0;
    border-bottom: 1px solid #e2e2e2;
    left: 0;
    position: absolute;
  }

  div.myrow{
    padding: 5px 0;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow : hidden;

    //span{
    //  display :inline-block;
    //  height :1em;
    //}

  }
}
</style>
