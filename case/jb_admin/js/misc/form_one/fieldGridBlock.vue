<template>
  <div class="com-fields-grid-block field-panel msg-bottom">
    <template v-for="head in heads">
        <div class="field-label" :class="head.class">
          <span class="req_star" v-if='head.required'>*</span>
          <div class="label-content" style="display: flex;align-items: center;">
            <span v-text="head.label"></span>
            <span>:</span>
          </div>
        </div>

        <div class="field-input" :class="head.class">
          <component v-if="head.editor" :is="head.editor"
                     @field-event="$emit('field-event',$event)"
                     :head="head" :row="row"></component>
          <span v-if="head.help_text" class="help-text clickable" @mouseenter="show_msg(head.help_text,$event)" @mouseleave="hide_msg()">
                                   <i style="color: #3780af;"   class="fa fa-question-circle" ></i>
                              </span>
        </div>

    </template>
  </div>
</template>
<script>

export default  {
  props:{
    heads:{},
    row:{},
    css:{},
  },
  computed:{
    table_grid_heads:function(){
      var self=this
      var table_grid = this.option.table_grid
      var heads_bucket =[]
      ex.each(table_grid,function(name_row){
        let heads_row =[]
        ex.each(self.heads,function(head){
          if(ex.isin(head.name,name_row)){
            heads_row.push(head)
          }
        })
        if(heads_row){
          heads_bucket.push(heads_row)
        }
      })
      return heads_bucket
    },
  },
  mounted(){
    if(this.css){
      ex.append_css(this.css)
    }
  },
  methods:{
    show_msg:function(msg,event){
      this.msg_index = layer.tips(msg, event.target,{
        time:0,
      });
    },
    hide_msg:function(){
      layer.close(this.msg_index)
    }
  }
}
</script>
<style scoped lang="scss">



.com-fields-table-block {
  &.field-panel {
    // 新的样式替换到了网格纹路的老样式
    padding-left:50px;
    margin-left:50px;
    border:none;
    box-shadow:none;
    position: relative;

  }
  /*
  主题
  */
  &.compact{
    padding-left:5px;
    margin-left:5px;
  }

  .field-label {
    display: flex;
    .label-content {
      min-width: 4em;
    }
    .req_star {
      position: relative;
      color: #f00;
    }
  }
  .field-input {
    padding-left: 12px;
    position: relative;
    display: flex;
    .help-text {
      display: inline-block;
      padding: 0 3px;
      position: relative;
      top: 6px;
    }
    span {
      &.readonly-info {
        color: #808080;
        height: 30px;
        display: inline-block;
        padding: 3px;
        line-height: 26px;
      }
    }
  }
}


</style>
