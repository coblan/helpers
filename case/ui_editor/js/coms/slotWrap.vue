<template>
  <div>
    我是 slot inn
    <component v-for="ii in children" :is="ii.editor" :key="ii.id" v-bind="ii.bind" :children="ii.children"></component>
  </div>
</template>
<script>
export default {
  props:{
    children:{
      default:()=>{}
    }
  }
}

cfg.ui_editor['uie-slot'] = {
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
  <div>容器,对应vue的slot功能</div>
  `
}
</script>