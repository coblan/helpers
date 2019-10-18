
Vue.component('com-chart-radar',{
    props:['ctx'],
    data:function(){
        return {
            barRows: [],
            rows:[],
            parStore:ex.vueParStore(this)
        }
    },
    template:` <div class="com-chart-plain com-chart-radar" style="height:400px;width: 500px;display: inline-block"></div>`,
    mounted:function(){
        //$('#mainjj').width($(this.$el).width()-30)
        //this. myChart = echarts.init(document.getElementById('mainjj'));
        this.myChart = echarts.init(this.$el);
        //this.getRows()
        this.parStore.$on('data-updated-backend',this.update_chart)
        this.update_chart()
    },
    methods:{
        update_chart(){
            var self=this
            if(this.ctx.source_rows){
                var rows = ex.eval(this.ctx.source_rows,{ps:this.parStore})
            }else{
                var rows = this.parStore.rows
            }

            var x_data=ex.map(rows,(row)=>{
                return {name:row[this.ctx.xdata],max:5000,min:-5000 }
            })


            var ydata_list = []
            var legend_list=[]
            debugger
            ex.each(this.ctx.ydata,(head)=>{
                var y_data=ex.map(rows,(row)=>{
                    return row[head.name]
                })
                ydata_list.push({
                    name:head.label,
                    value:y_data,
                    //itemStyle: {
                    //    normal: {
                    //        color: head.color // || '#27B6AC'
                    //    },
                    //},
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
                radar: {
                    // shape: 'circle',
                    name: {
                        textStyle: {
                            color: '#fff',
                            backgroundColor: '#999',
                            borderRadius: 3,
                            padding: [3, 5]
                        },
                    },
                    indicator:x_data,
                    //    [
                    //    { name: '销售（sales）', max: 6500},
                    //    { name: '管理（Administration）', max: 16000},
                    //    { name: '信息技术（Information Techology）', max: 30000},
                    //    { name: '客服（Customer Support）', max: 38000},
                    //    { name: '研发（Development）', max: 52000},
                    //    { name: '市场（Marketing）', max: 25000}
                    //]
                },
                //xAxis: {
                //    data: x_data
                //},
                //yAxis: {},
                series: [
                    {
                        name:'xxx',
                        type:'radar',
                        data:ydata_list

                    }
                ]
            };
            this.myChart.setOption(option);
        }
    },

})