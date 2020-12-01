require('./styl/datetime_range.styl')

var com_datetime_range={
    props:['head','search_args'],
    data:function(){
        //var start=this.search_args['_start_'+this.head.name]
        //var end=this.search_args['_end_'+this.head.name]
        return {
            heads:[
                {name:'_start_'+this.head.name,placeholder:'开始时间',clearable:this.head.clearable},
                {name:'_end_'+this.head.name,placeholder:'结束时间',clearable:this.head.clearable}
            ]
        }
    },
    template:`<div  class="com-filter-datetime-range flex flex-ac">
                <span v-text="head.label" style="white-space: nowrap"></span>:
                    <!--<input class="start form-control input-sm " v-model="start" readonly-->
                        <!--style="background-color: white;width: 12em"-->
                        <!--placeholder="开始时间">-->
                    <com-field-datetime :head="heads[0]" :row.sync="search_args"></com-field-datetime>
                    <div style="display: inline-block;margin: 0 2px;" >-</div>
                     <com-field-datetime :head="heads[1]" :row.sync="search_args"></com-field-datetime>
                    <!--<input class="end form-control input-sm"  v-model="end"  readonly-->
                     <!--style="background-color: white;width: 12em"-->
                     <!--placeholder="结束时间">-->
                </div>`,
    //mounted:function(){
    //    var self=this
    //    ex.load_js('/static/lib/laydate/laydate.js',function(){
    //        laydate.render({
    //            elem: $(self.$el).find('.start')[0],
    //            type: 'datetime',
    //            done: function(value, date, endDate){
    //                //self.search_args['_start_'+self.head.name]=value
    //                self.start = value
    //                //console.log(value); //得到日期生成的值，如：2017-08-18
    //                //console.log(date); //得到日期时间对象：{year: 2017, month: 8, date: 18, hours: 0, minutes: 0, seconds: 0}
    //                //console.log(endDate); //得结束的日期时间对象，开启范围选择（range: true）才会返回。对象成员同上。
    //            }
    //        });
    //        laydate.render({
    //            elem: $(self.$el).find('.end')[0],
    //            type: 'datetime',
    //            done: function(value, date, endDate){
    //                self.end=value
    //                //console.log(value); //得到日期生成的值，如：2017-08-18
    //                //console.log(date); //得到日期时间对象：{year: 2017, month: 8, date: 18, hours: 0, minutes: 0, seconds: 0}
    //                //console.log(endDate); //得结束的日期时间对象，开启范围选择（range: true）才会返回。对象成员同上。
    //            }
    //        });
    //    })
    //},
    computed:{
        start(){
            return this.search_args['_start_'+this.head.name]
        },
        end(){
            return this.search_args['_end_'+this.head.name]
        }
    },
    watch:{
        //start_value(v){
        //    this.start = v
        //},
        //end_value(v){
        //    this.end=v
        //},
        start:function(nv,ov){
            if(nv && this.end){
                if(nv>this.end){
                    cfg.showError('开始时间必须小于结束时间')

                    //this.search_args['_start_'+this.head.name] = ov
                    Vue.set(this.search_args,'_start_'+this.head.name,ov)
                }
            }
            //Vue.set(this.search_args,'_start_'+this.head.name,nv)

        },
        end:function(nv,ov){
            if(nv && this.start){
                if(nv<this.start){
                    cfg.showError('结束时间必须大于开始时间')
                    Vue.set(this.search_args,'_end_'+this.head.name,ov)
                    //var self=this
                    //Vue.nextTick(function(){
                    //    self.end = ov
                    //})
                    //return
                }
            }
            //Vue.set(this.search_args,'_end_'+this.head.name,nv)

        }
    },

}

Vue.component('com-filter-datetime-range',com_datetime_range)