
<template>
    <div class="live-table live-table-chart flex-v" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 2px;">
        <div v-if="childStore.row_filters.length > 0" style="background-color: #fbfbf8;padding: 8px 1em;border-radius: 4px;margin-top: 8px">
            <com-table-filters></com-table-filters>
        </div>
        <div  v-if="childStore.ops.length>0 ">
            <com-table-operations></com-table-operations>
        </div>

        <div v-if="childStore.parents.length>0">
            <com-table-parents></com-table-parents>
        </div>
        <div class="box box-success flex-v flex-grow" style="margin-bottom: 0">
            <div class="table-wraper flex-grow" style="position: relative;">

                <!--<component :is="ctx.inn_editor"></component>-->
                <template v-for="item in ctx.charts">
                    <component :is="item.editor" :ctx="item"></component>
                    <!--<div v-else  class="mychart" :class="'mychart-'+item.name" ></div>-->
                </template>


            </div>
        </div>
        <!--<div style="background-color: white;">-->
        <!--<com-table-pagination></com-table-pagination>-->
        <!--</div>-->
    </div>
</template>


<script>
    export default{
        props: ['ctx'],
        basename: 'live-table-chart',
        data: function () {
            var vc = this
            //var heads_ctx = this.ctx
            var my_table_store = {
                data: function () {
                    return {
                        head: vc.ctx,
                        heads: vc.ctx.heads,
                        row_filters: vc.ctx.row_filters,
                        row_sort: vc.ctx.row_sort,
                        director_name: vc.ctx.director_name,
                        footer: vc.ctx.footer || [],
                        ops: vc.ctx.ops || [],
                        rows: vc.ctx.rows || [],
                        row_pages: vc.ctx.row_pages || {},
                        selectable: vc.ctx.selectable == undefined ? true : vc.ctx.selectable,
                        selected: [],
                        del_info: [],
                        search_args: vc.ctx.search_args || {},
                        vc: vc,
                        parStore: ex.vueParStore(vc)
                    }
                },
                mixins: [table_store],
                watch: {
                    search_args: function (v) {
                        console.log(v)
                    }
                },
                methods: {}
            }
            return {
                childStore: new Vue(my_table_store),
                parStore: ex.vueParStore(vc),
            }
        },
        mounted: function () {
//            if (this.ctx.event_slots) {
//                ex.vueEventRout(this, this.ctx.event_slots)
//            }
            if (this.ctx.autoload == undefined || this.ctx.autoload ) {
                this.childStore.search().then(() => {
                    this.draw()
            })
            }


        },
        methods: {
            draw(){
                ex.each(this.ctx.charts, item => {
                    if(!item.editor){
                        this.draw_item(item)
                    }
                })
            },
            draw_item(item){
                debugger
                var myChart = echarts.init($(this.$el).find('.mychart-' + item.name)[0]);

                if (item.x) {
                    var myxlabel = this.childStore.rows.map(item => {return item[item.x]}
                ).
                    reverse()
                } else {
                    var myxlabel = []
                }
                var legend = []
                var series = []
                ex.each(item.y, y => {
                    var y_label = ex.findone(this.childStore.heads, {name: y}).label
                    legend.push(y_label)

                series.push(
                        {
                            name: y_label,
                            type: item.type,
                            data: this.childStore.rows.map(item => {return item[y]}).reverse(),
                        barMaxWidth
            :
                30,
                //itemStyle: {
                //    normal: {
                //        color:'#27B6AC'
                //    },
                //},

            }
            )
            })

                // 指定图表的配置项和数据
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
                    yAxis: {},
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




//Vue.component('com-live-table-type',live_table_type)
<style lang="scss" scoped>
    .mychart{
        padding: 10px;
        background-color: white;
        display:  inline-block;
        width: 500px;
        height: 350px;
    }

</style>
