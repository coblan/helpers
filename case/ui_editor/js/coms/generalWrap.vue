<template>
  <div :class="myclass">
    <component v-for="item in children" :is="item.editor" v-bind="item.bind"></component>
  </div>
</template>
<script>
export default {
  props:{
    myclass:{},
    css:{},
    children:[]
  },
  mounted(){
    ex.append_css(this.css)
  }
}

cfg.ui_editor['uie-general-wrap'] = {
  has_children:true,
  fields:[
    {name:'myclass',label:'类名',editor: 'com-field-linetext'},
    {name:'css',label:'css样式',editor:'com-field-blocktext'},

  ]
}
</script>

