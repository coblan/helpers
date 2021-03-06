var com_date_datetimefield_range={
    props:['head','search_args'],
    data:function(){
        if(! this.search_args['_start_'+this.head.name]){
            Vue.set(this.search_args,'_start_'+this.head.name,'')
            var start=''
        }else{
            var start=this.search_args['_start_'+this.head.name].slice(0,10)
            this.search_args['_start_'+this.head.name]= start +' 00:00:00'
        }
        if(! this.search_args['_end_'+this.head.name]){
            Vue.set(this.search_args,'_end_'+this.head.name,'')
            var end=''
        }else{
            var end=this.search_args['_end_'+this.head.name].slice(0,10)
            this.search_args['_end_'+this.head.name]=end+' 23:59:59'
        }
        return {
            start:start,
            end:end
        }
    },
    template:`<div  class="com-date-range-filter date-filter flex flex-ac">
                     <!--<date v-model="start" :placeholder="head.label"></date>-->
                     <span v-text="head.label" style="white-space: nowrap"></span>:
                        <input class="start form-control input-sm " v-model="start" readonly
                        style="background-color: white"
                        placeholder="开始日期">
                    <div style="display: inline-block;margin: 0 2px;" >-</div>
                        <!--<date  v-model="end" :placeholder="head.label"></date>-->
                        <input class="end form-control input-sm"  v-model="end"  readonly
                         style="background-color: white"
                         placeholder="结束日期">
                </div>`,
    mounted:function(){
        var self=this
        ex.load_js('/static/lib/laydate/laydate.js',function(){
            laydate.render({
                elem: $(self.$el).find('.start')[0],
                type: 'date',
                done: function(value, date, endDate){
                    //self.search_args['_start_'+self.head.name]=value
                    self.start=value
                }
            });
            laydate.render({
                elem: $(self.$el).find('.end')[0],
                type: 'date',
                done: function(value, date, endDate){
                    //self.search_args['_end_'+self.head.name]=value
                    self.end=value
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
            this.start = v.slice(0,10)
        },
        end_value(v){
            this.end=v.slice(0,10)
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
            if(nv && nv.length <19){

                Vue.set(this.search_args,'_start_'+this.head.name ,nv+' 00:00:00')
            }else{
                Vue.set(this.search_args,'_start_'+this.head.name,nv)
            }
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
            if(nv && nv.length <19){
                Vue.set(this.search_args,'_end_'+this.head.name,nv+' 23:59:59')
            }else{
                Vue.set(this.search_args,'_end_'+this.head.name,nv)
            }
        }
    },

}
window.com_date_datetimefield_range=com_date_datetimefield_range
Vue.component('com-date-datetimefield-range-filter',com_date_datetimefield_range)
