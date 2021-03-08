<template>
    <div  class="com-chart-general" :class="ctx.class">
        <div  class="mychart" ></div>
    </div>

</template>
<script>
    export default {
        props:['ctx'],
        data(){
            return {
                parStore: ex.vueParStore(this),
                rows:this.ctx.rows || [],
            }
        },
        mounted(){
            if(this.ctx.css){
                ex.append_css(this.ctx.css)
            }
            if(this.ctx.mounted_express){
                ex.eval(this.ctx.mounted_express,{vc:this})
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
                    var myxlabel = this.rows.map(item => {return item[this.ctx.x]} ). reverse()
                } else {
                    var myxlabel = []
                }
                var legend = []
                var series = []
                ex.each(this.ctx.y, y => {
//                    var y_label = ex.findone(this.parStore.heads, {name: y.name}).label
                    var y_label = y.label
                    legend.push(y_label)

                series.push(
                        {
                            name: y_label,
                            type: y.type || 'bar',
                            yAxisIndex: y.axisIndex|| 0,
                            data: this.rows.map(item => {return item[y.name]}).reverse(),
                        barMaxWidth:y.barMaxWidth || 30,
                        itemStyle: {
                            normal: {
                                color:y.color
                            }
                        },

            }
            )
            })

                // 指定图表的配置项和数据

//                var yaxis = {
//                    axisLabel: {
//                        margin: 2,
//                        formatter: function (value, index) {
//                            var ab_value = Math.abs(value)
//                            if ( ab_value >= 10000 && ab_value < 10000000) {
//                                value = value / 10000 + "万";
//                            } else if (ab_value >= 10000000) {
//                                value = value / 10000000 + "千万";
//                            }
//                            return value;
//                        }
//                    },
//                }


                var option = {
                    title: {
                        text: this.ctx.label,
                        textStyle: {
                            fontWeight: 'normal',
                            fontSize: 14,
                        }
                    },

                    tooltip: {},
                    legend: {
                        data: legend //['用户数']
                    },
//                    grid:{
//                        left:"20%"
//                    },
                    xAxis: {
                        type: 'value',
                    },
                    yAxis: {
                        type: 'category',
                        data: myxlabel,
//                        axisLabel: {
//                            interval: 0,
//                            rotate: 30
//                        },
                    },
                    series: series,
                };

                if(this.ctx.option_express){
                    ex.eval(this.ctx.option_express,{option:option})
                }
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
