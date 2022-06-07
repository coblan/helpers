<template>
  <pie :class="myclass" ref="chart" :kvList="kvlist"  :title="title"></pie>
</template>
<script>
import pie from 'webcase/chart/pie.vue'
import ex from 'weblib/ex'
export default {
  components:{
    pie
  },
  props:{
    director:{},
    myclass:{},
  },
  data(){
    return {
      kvlist:[],
      title:''
    }
  },
  async mounted(){
    var resp = await ex.director_get(this.director)
    this.kvlist=resp.kvlist
    this.title=resp.title
    this.$nextTick(()=>{
      this.$refs.chart.draw()
    })
  },
}

cfg.ui_editor['uie-pie'] = {
  fields:[
    {name:'director',label:'director',editor: 'com-field-linetext'},
    {name:'myclass',label:'类名',editor: 'com-field-split-text',splitter:' ',
      options:[
        {value:'flex',label:'flex'},
      ]},
    {name:'css',label:'css样式',editor:'com-field-blocktext'},

  ],
  desp:'Echarts pie图',
  help_text:`
<div>数据结构</div>
<pre>
  title:{},
  kvlist:[
         { "value": 1048, "name": 'Search Engine' },
         { "value": 735, "name": 'Direct' },
        { "value": 580, "name": 'Email' },
  ]
</pre>
<img src="/static/uie/pie.png" alt="">
  `
}
</script>