<template>
  <div :class="myclass">
    <component v-for="item in children" :is="item.editor" :key="item.id" v-bind="item.bind" :id="item.id" :children="item.children"></component>
  </div>
</template>
<script>
export default {
  props:{
    myclass:{},
    css:{},
    children:{}
  },
  mounted(){
    ex.append_css(this.css)
  },
  computed:{
    // validCss(){
    //   return this.myclass.split(',')
    // }
  }
}

cfg.ui_editor['uie-general-wrap'] = {
  has_children:true,
  fields:[
    {name:'myclass',label:'类名',editor: 'com-field-split-text',splitter:' ',
    options:[
      {value:'flex',label:'flex'},
    ]},
    {name:'css',label:'css样式',editor:'com-field-blocktext'},

  ],
  desp:'容器',
  help_text:`
  <div>容器，可以flex,grid等布局</div>
  `
}
</script>

