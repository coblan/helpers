require('./styl/chart.styl')

Vue.component('com-chart-plain',{
    props:['ctx'],
    data:function(){
        return {
            barRows: [],
            rows:[],
            parStore:ex.vueParStore(this)
        }
    },
    template:` <div class="com-chart-plain" :class="ctx.class" :style="ctx.style"></div>`,
    mounted:function(){
        //$('#mainjj').width($(this.$el).width()-30)
        //this. myChart = echarts.init(document.getElementById('mainjj'));
        this.myChart = echarts.init(this.$el);
        //this.getRows()
        this.parStore.$on('data-updated-backend',this.update_chart)
        if(this.ctx.css){
            ex.append_css(this.ctx.css)
        }

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
            if(this.ctx.source_rows){
                var rows = ex.eval(this.ctx.source_rows,{ps:this.parStore})
            }else{
                var rows = this.parStore.rows
            }
            if(this.ctx.xdata){
                var x_data=ex.map(rows,(row)=>{
                    return row[this.ctx.xdata]
                })
            }else {
                var x_data = ex.eval(this.ctx.xdata_express,{rows:rows})
            }

            var ydata_list = []
            var legend_list=[]
            if(this.ctx.ydata){
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
                                color: head.color // || '#27B6AC'
                            },
                        },
                    })
                    legend_list.push(head.label)
                })
            }else{
                ex.eval(this.ctx.ydata_express,{rows:rows,ydata_list:ydata_list,legend_list:legend_list})
            }

            var option = {
                title: {
                    text: self.ctx.title,
                },
                tooltip: {},
                legend: {
                    data:legend_list
                },
                xAxis: {
                    data: x_data,
                },
                yAxis: {},
                series: ydata_list
            };
            if(this.ctx.echarts_option){
                ex.mergeObject(option,this.ctx.echarts_option)
            }

            //if(this.ctx.x_interval != undefined){
            //    var axisLabel={
            //        interval:this.ctx.x_interval,//横轴信息全部显示
            //        fontSize:10,
            //        //formatter:function(value){//只显示7个字 其余省略号
            //        //    //return value.length > 7?value.substring(0,7)+'...':value;
            //        //    var out=''
            //        //    for(var i=0;i<value.length;i+=7){
            //        //        out+= value.substring(i,i+7)+'\n'
            //        //    }
            //        //    return out
            //        //    //return value.length > 7?value.substring(0,7)+'...':value;
            //        //},
            //        //formatter: [
            //        //    '{mylabel|这段文本采用样式mylabel}',
            //        //
            //        //].join('\n'),
            //        //formatter:  '{a|{value}a}',
            //                //formatter:function(val){
            //                //    return val.split("").join("\n");
            //                //},
            //        //rich: {
            //        //    a: {
            //        //        color: 'red',
            //        //        textOverflow:'ellipsis',
            //        //        width:'100px'
            //        //    },
            //        //}
            //    }
            //    if(this.ctx.x_rotate){
            //        axisLabel.rotate = this.ctx.x_rotate
            //    }
            //    option.xAxis.axisLabel = axisLabel
            //}


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