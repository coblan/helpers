<template>
    <div  class="com-chart-type-bar" :class="ctx.class">
        <div  class="mychart" ></div>
    </div>

</template>
<script>
    export default {
        /*
        *
        * */
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

//                if (this.ctx.x) {
//                    var myxlabel = this.rows.map(item => {return item[this.ctx.x]} ). reverse()
//                } else {
//                    var myxlabel = []
//                }
//                var legend = []
//                var series = []
//                ex.each(this.ctx.y, y => {
////                    var y_label = ex.findone(this.parStore.heads, {name: y.name}).label
//                    var y_label = y.label
//                    legend.push(y_label)
//
//                series.push(
//                        {
//                            name: y_label,
//                            type: y.type || 'bar',
//                            yAxisIndex: y.axisIndex|| 0,
//                            data: this.rows.map(item => {return item[y.name]}).reverse(),
//                        barMaxWidth:30,
//                        itemStyle: {
//                    normal: {
//                        color:y.color
//                    }
//                },
//
//            }
//            )
//            })

                // 指定图表的配置项和数据
//
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
//                if(this.ctx.yAxis ){
//                    ex.each(this.ctx.yAxis,axe=>{
//                        ex.assign(axe,yaxis)
//                })
//
//                }
//
//                var option = {
//                    title: {
//                        text: ''
//                    },
//                    tooltip: {},
//                    legend: {
//                        data: legend //['用户数']
//                    },
//                    xAxis: {
//                        data: myxlabel // this.childStore.rows.map(item=>{return item[item.x]}).reverse()
//                        //data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
//                    },
//                    yAxis: this.ctx.yAxis || yaxis,
//                    series: series,
//                };


                var option = {
                    dataset: {
                        source: [
                            ['score', 'amount', 'product'],
                            [89.3, 58212, 'Matcha Latte'],
                            [57.1, 78254, 'Milk Tea'],
                            [74.4, 41032, 'Cheese Cocoa'],
                            [50.1, 12755, 'Cheese Brownie'],
                            [89.7, 20145, 'Matcha Cocoa'],
                            [68.1, 79146, 'Tea'],
                            [19.6, 91852, 'Orange Juice'],
                            [10.6, 101852, 'Lemon Juice'],
                            [32.7, 20112, 'Walnut Brownie'],
                            [89.3, 58212, 'Matcha Latte2'],
                            [57.1, 78254, 'Milk Tea2'],
                            [74.4, 41032, 'Cheese Cocoa2'],
                            [50.1, 12755, 'Cheese Brownie2'],
                            [89.7, 20145, 'Matcha Cocoa2'],
                            [68.1, 79146, 'Tea2'],
                            [19.6, 91852, 'Orange Juice2'],
                            [10.6, 101852, 'Lemon Juice2'],
                            [32.7, 20112, 'Walnut Brownie2']
                        ]
                    },
                    title: {
                        text: this.ctx.label,
                        x:'center',
                        y:'top',
                        textStyle: {
                            fontWeight: 'normal',
                            fontSize: 14,
                        }

                    },
                    grid: {containLabel: true},
                    xAxis: {name: 'amount'},
                    yAxis: {type: 'category'},
//                    visualMap: {
//                        orient: 'horizontal',
//                        left: 'center',
//                        min: 10,
//                        max: 100,
//                        text: ['High Score', 'Low Score'],
//                        // Map the score column to color
//                        dimension: 0,
//                        inRange: {
//                            color: ['#D7DA8B', '#E15457']
//                        }
//                    },
                    series: [
                        {
                            type: 'bar',
                            encode: {
                                // Map the "amount" column to X axis.
                                x: this.ctx.x, //'amount',
                                // Map the "product" column to Y axis
                                y: this.ctx.y, //'product'
                            }
                        }
                    ]
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
