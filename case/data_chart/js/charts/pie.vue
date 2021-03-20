<template>
    <div  class="com-chart-pie" :class="ctx.class">
        <div  class="mychart" ></div>
    </div>
</template>

<script>
    /*
    options 参考网址 https://echarts.apache.org/examples/zh/editor.html?c=pie-simple
    * */
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
            setTimeout(()=>{
                this.draw()
            },20)

        },
        watch:{
            rows(){
                this.draw()
            }
        },
        methods:{
            draw(){
                var myChart = echarts.init($(this.$el).find('.mychart')[0]);

                var option = {
                    title: {
                        text: this.ctx.title,
                        subtext: this.ctx.subtitle,
                        textStyle: {
                            fontSize: 14,
                            fontWeight:'normal',
                        },
//                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'item'
                    },
//                    legend: {
//                        orient: 'vertical',
//                        left: 'left',
//                    },
                    series: [
                        {
//                            name: '访问来源',
                            type: 'pie',
                            radius: '60%',
                            color:this.ctx.color,
                            data:this.ctx.rows,
//                            data: [
//                                {value: 1048, name: '搜索引擎'},
//                                {value: 735, name: '直接访问'},

//                            ],
                            emphasis: {
                                itemStyle: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                },
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
    .com-chart-pie{
        display: inline-block;
    }
</style>