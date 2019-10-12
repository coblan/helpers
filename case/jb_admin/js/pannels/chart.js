
Vue.component('com-chart-plain',{
    props:['ctx'],
    data:function(){
        return {
            barRows: [],
            parStore:ex.vueParStore(this)
        }
    },
    template:` <div class="com-chart-plain" style="height:400px;width: 500px;display: inline-block"></div>`,
    mounted:function(){
        //$('#mainjj').width($(this.$el).width()-30)
        //this. myChart = echarts.init(document.getElementById('mainjj'));
        this.myChart = echarts.init(this.$el);
        //this.getRows()
        this.parStore.$on('data-updated-backend',this.update_chart)


    },
    methods:{
        //getRows:function(){
        //    var self=this
        //    cfg.show_load()
        //    ex.director_call('trend_data',{key:this.trend.key},function(resp){
        //        self.barRows=resp
        //        cfg.hide_load()
        //    })
        //}
        update_chart(){
            var self=this
            var rows = this.parStore.rows
            var x_data=ex.map(rows,(row)=>{
                return row[this.ctx.xdata]
            })


            var ydata_list = []
            var legend_list=[]
            ex.each(this.ctx.ydata,(head)=>{
                var y_data=ex.map(rows,(row)=>{
                    return row[head.name]
                })
                ydata_list.push({
                    name:head.label,
                    type:head.type,
                    data:y_data,
                    barMaxWidth: 30,
                    itemStyle: {
                        normal: {
                            color: head.color || '#27B6AC'
                        },
                    },
                })
                legend_list.push(head.label)
            })

            var option = {
                title: {
                    text: self.ctx.title,
                },
                tooltip: {},
                legend: {
                    data:legend_list
                },
                xAxis: {
                    data: x_data
                },
                yAxis: {},
                series: ydata_list
            };
            this.myChart.setOption(option);
        }
    },
    watch:{
        barRows:function(v){
            var self=this
            var x_data=ex.map(v,function(item){
                return item.time
            })
            var y_data=ex.map(v,function(item){
                return item.amount
            })

            var option = {
                title: {
//                text: 'ECharts 入门示例'
                },
                tooltip: {},
//            legend: {
//                data:['销量']
//            },
                xAxis: {
                    data: x_data
                },
                yAxis: {},
                series: [{
                    name: self.trend.label,
                    type: 'bar',
                    data: y_data,
                }]
            };
            this.myChart.setOption(option);
        }
    }
})