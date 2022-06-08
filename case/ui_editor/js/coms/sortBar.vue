<template>
  <sortBar :class="myclass" ref="chart"
            :title="title" :ydata="ydata" :xdata="xdata"></sortBar>
</template>

<script>
import sortBar from "webcase/chart/sortBar.vue";
import  ex from 'weblib/ex'
export default {
  components:{
    sortBar
  },
  props:{
    title: {},
    ydata:{},
    xdata:{},
    myclass:{},
    // ctxName:{},
    // director:{},
  },

  // data(){
  //   return {
  //     row:{
  //       title:'',
  //       ydata:[],
  //       xdata:[],
  //     }
  //
  //   }
  // },

  async mounted(){
    // if(this.ctxName && named_ctx[this.ctxName]){
    //   var ctx = named_ctx[this.ctxName]
    //   ex.vueAssign(this.row,ctx)
    // }else if(this.director){
    //   var resp = await ex.director_call(this.director,)
    //   ex.vueAssign(this.row,resp)
    // }
    this.$refs.chart.draw()
  }
}

cfg.ui_editor['uie-sortBar'] = {
  has_bind_express: true,
  fields:[
    // {name:'bind_express',label:'绑定脚本',editor: 'com-field-blocktext'},
    // {name:'ctxName',label:'ctxName',editor: 'com-field-linetext'},
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