<template>
    <div  class="com-table-chart-general" :class="ctx.class">
        <div  class="mychart" ></div>
    </div>

</template>
<script>
 export default {
     props:['ctx'],
     data(){
         return {
             parStore: ex.vueParStore(this)
         }
     },
     mounted(){
        if(this.ctx.css){
            ex.append_css(this.ctx.css)
        }
     },
     computed:{
         rows(){
             if(this.parStore){
                 return this.parStore.rows
             }else{
                 return []
             }
         }
     },
     watch:{
         rows(){
             this.draw()
         }
     },
     methods:{
         draw(){
             var myChart = echarts.init($(this.$el).find('.mychart')[0]);
             if (this.ctx.x) {
                 var myxlabel = this.parStore.rows.map(item => {return item[this.ctx.x]} ). reverse()
             } else {
                 var myxlabel = []
             }
             var legend = []
             var series = []
             ex.each(this.ctx.y, y => {
                 var y_label = ex.findone(this.parStore.heads, {name: y.name}).label
                 legend.push(y_label)

             series.push(
                     {
                         name: y_label,
                         type: y.type || 'bar',
                         yAxisIndex: y.axisIndex|| 0,
                         data: this.parStore.rows.map(item => {return item[y.name]}).reverse(),
                     barMaxWidth:30,
                     itemStyle: {
                         normal: {
                             color:y.color
                         }
                     },
             //itemStyle: {
             //    normal: {
             //        color:'#27B6AC'
             //    },
             //},

         }
         )
         })

             // 指定图表的配置项和数据

             var yaxis = {
                 axisLabel: {
                     margin: 2,
                     formatter: function (value, index) {
                         var ab_value = Math.abs(value)
                         if ( ab_value >= 10000 && ab_value < 10000000) {
                             value = value / 10000 + "万";
                         } else if (ab_value >= 10000000) {
                             value = value / 10000000 + "千万";
                         }
                         return value;
                     }
                 },
             }
             if(this.ctx.yAxis ){
                 ex.each(this.ctx.yAxis,axe=>{
                     ex.assign(axe,yaxis)
                 })

             }

             var option = {
                 title: {
                     text: ''
                 },
                 tooltip: {},
                 legend: {
                     data: legend //['用户数']
                 },
                 xAxis: {
                     data: myxlabel // this.childStore.rows.map(item=>{return item[item.x]}).reverse()
                     //data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
                 },
                 yAxis: this.ctx.yAxis || yaxis,
                 series: series,
                 //    [{
                 //    name: '用户数',
                 //    type: 'bar',
                 //    data: this.parStore.rows.map(item=>{return item.betusernum}).reverse(),
                 //    barMaxWidth: 30,
                 //    itemStyle: {
                 //        normal: {
                 //            color:'#27B6AC'
                 //        },
                 //    },
                 //
                 //}]
             };

             // 使用刚指定的配置项和数据显示图表。
             myChart.setOption(option);
         }
     }
 }
</script>

<style scoped lang="scss">
    .com-table-chart-general{
        display: inline-block;
    }
</style>
