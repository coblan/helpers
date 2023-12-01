<template>
  <div class="com-fields-grid-block field-panel msg-bottom">
    <template v-if="type=='line'">
      <template  v-for="head in heads">
        <div class="field-label" :class="[head.class,`label-${head.name}`]">
          <span class="req_star" v-if='head.required'>*</span>
          <div class="label-content" style="display: flex;align-items: center;">
            <span v-text="head.label"></span>
            <span>:</span>
          </div>
        </div>

        <div class="field-input" :class="[head.class,`input-${head.name}`]" >
          <div style="position: relative">
            <component v-if="head.editor"
                       :is="head.editor"
                       @field-event="$emit('field-event',$event)"
                       :head="head" :row="row"></component>
            <span v-if="head.help_text"
                  class="help-text clickable" @mouseenter="show_msg(head.help_text,$event)" @mouseleave="hide_msg()">
                   <i style="color: #3780af;"   class="fa fa-question-circle" ></i>
             </span>
          </div>
        </div>
      </template>
    </template>

    <template v-else>
      <div class="field-stack" :class="[`stack-${head.name}`]"   v-for="head in heads">
        <div class="field-label" :class="[head.class,`label-${head.name}`]">
          <div class="label-content" style="display: flex;align-items: center;line-height: 40px;gap: 10px;">
            <span v-text="head.label"></span>
            <span class="req_star" v-if='head.required'>*</span>

            <span v-if="head.help_text"
                  class="help-text clickable" @mouseenter="show_msg(head.help_text,$event)" @mouseleave="hide_msg()">
                 <i style="color: #3780af;"   class="fa fa-question-circle" ></i>
           </span>
          </div>
        </div>
        <div class="field-input" :class="[head.class,`input-${head.name}`]" >
            <component v-if="head.editor"
                       :is="head.editor"
                       @field-event="$emit('field-event',$event)"
                       :head="head" :row="row"></component>
        </div>
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
    type:{
      default:'line', // stack
    },
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

.field-label {
  display: flex;
  padding-top: 5px;
  .label-content {
    min-width: 4em;
  }
  .req_star {
    position: relative;
    color: #f00;
  }
}
.field-input {
  //padding-left: 12px;
  position: relative;
  width: 100%;
  .help-text {
    display: inline-block;
    padding: 0 3px;
    position: absolute;
    right: -27px;
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

.com-fields-grid-block{
  ::v-deep{
    .el-select{
      width: 100%;
    }
    .el-cascader{
      width: 100%;
      input{
        width: 100%;
      }
    }
  }
}


</style>
