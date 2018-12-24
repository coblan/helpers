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
                     <date v-model="start" :placeholder="head.label"></date>
                    <div style="display: inline-block;margin: 0 2px;" >-</div>
                        <date  v-model="end" :placeholder="head.label"></date>
                </div>`,

    watch:{
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
            if(nv){
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
            if(nv){
                Vue.set(this.search_args,'_end_'+this.head.name,nv+' 23:59:59')
            }else{
                Vue.set(this.search_args,'_end_'+this.head.name,nv)
            }
        }
    },

}
window.com_date_datetimefield_range=com_date_datetimefield_range
Vue.component('com-date-datetimefield-range-filter',com_date_datetimefield_range)
