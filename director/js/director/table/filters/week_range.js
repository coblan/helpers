
var week_range={
    props:['head','search_args'],
    data:function(){

        var start=this.search_args['_start_'+this.head.name]
        var end=this.search_args['_end_'+this.head.name]
        return {
            start:start,
            end:end
        }
    },
    template:`<div  class="com-filter-week-range flex flex-ac">
     <span v-text="head.label" style="white-space: nowrap"></span>:
             <el-date-picker
              v-model="start"
              type="week"
              size="small"
              format="yyyy 第 WW 周"
              placeholder="开始周">
            </el-date-picker>

                    <!--<input class="start form-control input-sm " v-model="start" readonly-->
                        <!--style="background-color: white;width: 12em"-->
                        <!--placeholder="开始月份">-->
                    <div style="display: inline-block;margin: 0 2px;" >-</div>
                    <el-date-picker
                  v-model="end"
                  type="week"
                  size="small"
                  format="yyyy 第 WW 周"
                  placeholder="结束周">
                </el-date-picker>
                    <!--<input class="end form-control input-sm"  v-model="end"  readonly-->
                     <!--style="background-color: white;width: 12em"-->
                     <!--placeholder="结束月份">-->
                </div>`,
    mounted:function(){
        var self=this
        ex.load_js('/static/lib/laydate/laydate.js',function(){
            laydate.render({
                elem: $(self.$el).find('.start')[0],
                type: 'week',
                done: function(value, date, endDate){
                    //self.search_args['_start_'+self.head.name]=value
                    self.start = value
                    //console.log(value); //得到日期生成的值，如：2017-08-18
                    //console.log(date); //得到日期时间对象：{year: 2017, month: 8, date: 18, hours: 0, minutes: 0, seconds: 0}
                    //console.log(endDate); //得结束的日期时间对象，开启范围选择（range: true）才会返回。对象成员同上。
                }
            });
            laydate.render({
                elem: $(self.$el).find('.end')[0],
                type: 'week',
                done: function(value, date, endDate){
                    self.end=value
                    //console.log(value); //得到日期生成的值，如：2017-08-18
                    //console.log(date); //得到日期时间对象：{year: 2017, month: 8, date: 18, hours: 0, minutes: 0, seconds: 0}
                    //console.log(endDate); //得结束的日期时间对象，开启范围选择（range: true）才会返回。对象成员同上。
                }
            });
        })
    },
    computed:{
        start_value(){
            return this.search_args['_start_'+this.head.name]
        },
        end_value(){
            return this.search_args['_end_'+this.head.name]
        }
    },
    watch:{
        start_value(v){
            //this.start = v
        },
        end_value(v){
            //this.end=v
        },
        start:function(nv,ov){
            if(nv && this.end){
                if(nv>this.end){
                    cfg.showError('开始时间必须小于结束时间')
                    var self=this
                    Vue.nextTick(function(){
                        self.start = ov
                    })
                    return
                }
            }
            Vue.set(this.search_args,'_start_'+this.head.name,moment(nv).format('YYYY-MM-DD') )

        },
        end:function(nv,ov){
            if(nv && this.start){
                if(nv<this.start){
                    cfg.showError('结束时间必须大于开始时间')
                    var self=this
                    Vue.nextTick(function(){
                        self.end = ov
                    })
                    return
                }
            }
            Vue.set(this.search_args,'_end_'+this.head.name,moment(nv).format('YYYY-MM-DD'))

        }
    },

}

Vue.component('com-filter-week-range',week_range)
