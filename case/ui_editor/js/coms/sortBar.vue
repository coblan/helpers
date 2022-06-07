<template>
  <div>
    hello
  </div>
</template>

<script>
export default {

}

cfg.ui_editor['uie-sortBar'] = {
  fields:[
    {name:'myclass',label:'类名',editor: 'com-field-split-text',splitter:' ',
      options:[
        {value:'flex',label:'flex'},
      ]},
    {name:'css',label:'css样式',editor:'com-field-blocktext'},

  ],
  desp:'Echarts排名'
}
</script>