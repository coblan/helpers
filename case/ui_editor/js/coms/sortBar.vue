<template>
  <sortBar  style="width: 500px;height: 300px;margin: 10px;background-color: white"
            title="加油金额排名" :ydata="['装备验收员','装备技师',]" :xdata="[{name:'',data:[1011,1800,]}]"></sortBar>
</template>

<script>
import sortBar from "webcase/chart/sortBar.vue";
export default {
  components:{
    sortBar
  }
}

cfg.ui_editor['uie-sortBar'] = {
  fields:[
    {name:'director',label:'director',editor: 'com-field-linetext'},
    {name:'myclass',label:'类名',editor: 'com-field-split-text',splitter:' ',
      options:[
        {value:'flex',label:'flex'},
      ]},
    {name:'css',label:'css样式',editor:'com-field-blocktext'},

  ],
  desp:'Echarts排名',
  help_text:`
<div>数据结构</div>
<pre>
  title:{},
  ydata:{}, //['Brazil', 'Indonesia', 'USA', 'India', 'China', 'World']
   xdata:{}   [
                {
                   name: '2011',
                   data: [18203, 23489, 29034, 104970, 131744, 630230]
                },
              ]
</pre>
<img src="/static/uie/sortBar.png" alt="">
  `
}
</script>