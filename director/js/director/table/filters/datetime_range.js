
var com_datetime_range={
    props:['head','search_args'],
    data:function(){
        if(! this.search_args['_start_'+this.head.name]){
            Vue.set(this.search_args,'_start_'+this.head.name,'')
        }
        if(! this.search_args['_end_'+this.head.name]){
            Vue.set(this.search_args,'_end_'+this.head.name,'')
        }
        return {

        }
    },
    template:`<div  class="com-filter-datetime-range flex flex-ac">
                    <input class="start form-control input-sm " v-model="search_args['_start_'+head.name]" readonly
                        style="background-color: white"
                        :placeholder="head.label">
                    <div style="display: inline-block;margin: 0 2px;" >-</div>
                    <input class="end form-control input-sm"  v-model="search_args['_end_'+head.name]"  readonly
                     style="background-color: white"
                     :placeholder="head.label">
                </div>`,
    //template:`<div  class="com-filter-datetime flex flex-ac">
    //                <input type="text" class="form-control input-sm" style="width: 23em" readonly
    //                    :placeholder="head.placeholder">
    //            </div>`,
    mounted:function(){
        var self=this
        ex.load_js('/static/lib/laydate/laydate.js',function(){
            laydate.render({
                elem: $(self.$el).find('.start')[0],
                type: 'datetime',
                done: function(value, date, endDate){
                    self.search_args['_start_'+self.head.name]=value
                    //console.log(value); //得到日期生成的值，如：2017-08-18
                    //console.log(date); //得到日期时间对象：{year: 2017, month: 8, date: 18, hours: 0, minutes: 0, seconds: 0}
                    //console.log(endDate); //得结束的日期时间对象，开启范围选择（range: true）才会返回。对象成员同上。
                }
            });
            laydate.render({
                elem: $(self.$el).find('.end')[0],
                type: 'datetime',
                done: function(value, date, endDate){
                    self.search_args['_end_'+self.head.name]=value
                    //console.log(value); //得到日期生成的值，如：2017-08-18
                    //console.log(date); //得到日期时间对象：{year: 2017, month: 8, date: 18, hours: 0, minutes: 0, seconds: 0}
                    //console.log(endDate); //得结束的日期时间对象，开启范围选择（range: true）才会返回。对象成员同上。
                }
            });
        })
    }

}

Vue.component('com-filter-datetime-range',com_datetime_range)