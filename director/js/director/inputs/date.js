/**
 * Created by heyulin on 2017/1/24.
 *
 >->front/input.rst>
 =======
 inputs
 =======

 date
 ========
 ::

 <date v-model='variable'></date>  // 选择默认set=date ,即选择日期

 <date v-model='variable' set='month'></date> // 选择 set=month ,即选择月份

 <date v-model='variable' set='month' :config='{}'></date>  //  config 是自定义的配置对象，具体需要参加帮助文件

 datetime
 ===========
 ::

 <datetime v-model='variable' :config='{}'></datetime> // 选择日期和时间

 color
 ======

 forign-edit
 ============
 示例::

 <forign-edit :kw="person.emp_info" name="user" page_name="user" ></forign-edit>

 <-<
 */



var date_config_set={
    date:{
        language: "zh-CN",
        format: "yyyy-mm-dd",
        autoclose: true,
        todayHighlight: true,

    },
    month:{
        language: "zh-CN",
        format: "yyyy-mm",
        startView: "months",
        minViewMode: "months",
        autoclose: true,
    },
}

var com_input_date = {
    //template:'<input type="text" class="form-control">',
    template:` <div class="com-date input-group datetime-picker">
                <input type="text" class="form-control input-sm real-input"
                readonly :placeholder="placeholder"/>

                <div class="input-group-addon" >
                    <i v-if="! value" @click="click_input()" class="fa fa-calendar" aria-hidden="true"></i>
                    <i v-else @click="$emit('input','')" class="fa fa-calendar-times-o" aria-hidden="true"></i>
                </div>
                </div>`,
    props:['value','set','config','placeholder'],
    mounted:function () {
        this.init()
    },
    methods:{
        init:function(){
            var self=this
            if(!this.set){
                var def_conf=date_config_set.date
            }else{
                var def_conf=date_config_set[this.set]
            }
            if(this.config){
                ex.assign(def_conf,this.config)
            }
            self.input=$(this.$el).find('input')

            ex.load_css('/static/lib/bootstrap-datepicker1.6.4.min.css')

            //ex.load_js('/static/lib/bootstrap-datepicker1.6.4.min.js',function(){
            //    ex.load_js('/static/lib/bootstrap-datepicker1.6.4.zh-CN.min.js',function(){
            //        self.input.datepicker(def_conf).on('changeDate', function(e) {
            //            self.$emit('input',self.input.val())
            //        })
            //        // if has init value,then init it
            //        if(self.value){
            //            self.input.datepicker('update',self.value)
            //            self.input.val(self.value)
            //        }
            //    })
            //})
            ex.load_js('/static/lib/bootstrap-datepicker1.6.4.min.js').then(function(){
                return ex.load_js('/static/lib/bootstrap-datepicker1.6.4.zh-CN.min.js')
            }).then(function(){
                    self.input.datepicker(def_conf).on('changeDate', function(e) {
                        self.$emit('input',self.input.val())
                    })
                    // if has init value,then init it
                    if(self.value){
                        self.input.datepicker('update',self.value)
                        self.input.val(self.value)
                    }
            })
        },
        click_input:function(){
            this.input.focus()
        },
        watch_value:function(n){
            this.input.datepicker('update',n)
            this.input.val(n)
        }
    },
    watch:{
        value:function (n) {
            this.watch_value(n)
        }
    }
}
window.com_input_date=com_input_date
Vue.component('date',com_input_date)



Vue.component('datetime',{
    template:` <div class="com-datetime input-group datetime-picker">
                <input type="text" class="form-control input-sm" readonly :placeholder="placeholder"/>
                <div class="input-group-addon" >
                    <i v-if="! value" @click="click_input()" class="fa fa-calendar" aria-hidden="true"></i>
                    <i v-else @click="$emit('input','')" class="fa fa-calendar-times-o" aria-hidden="true"></i>
                </div>
                </div>`,

    //props:['value','config'],
    props:['value','set','config','placeholder'],
    mounted:function () {
        var self=this
        var def_conf={
            language: "zh-CN",
            format: "yyyy-mm-dd hh:ii",
            autoclose: true,
            todayHighlight: true,
            minuteStep:1,
        }
        if(self.config){
            ex.assign(def_conf,this.config)
        }
        self.input=$(this.$el).find('input')

        ex.load_css('/static/lib/smalot-bootstrap-datetimepicker2.4.3.min.css')
        ex.load_js('/static/lib/moment2.17.1.min.js')
        ex.load_js('/static/lib/smalot-bootstrap-datetimepicker2.4.3.min.js',function(){

            $.fn.datetimepicker.dates['zh-CN'] = {
                days: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"],
                daysShort: ["周日", "周一", "周二", "周三", "周四", "周五", "周六", "周日"],
                daysMin:  ["日", "一", "二", "三", "四", "五", "六", "日"],
                months: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                monthsShort: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                today: "今天",
                suffix: [],
                meridiem: ["上午", "下午"]
            };

            self.input.datetimepicker(def_conf).on('changeDate', function(e) {
                self.$emit('input',self.input.val())
            })

            // if has init value,then init it
            if(self.value){
                self.input.datepicker('update',self.value)
                self.input.val(self.value)
            }

        })
    },
    methods:{
        click_input:function(){
            this.input.focus()
        }
    },
    watch:{
        value:function (n) {
            this.input.val(n)
            this.input.val(n)
        },
        //input_value:function(n){
        //    this.$emit('input',n)
        //}
    }
})


