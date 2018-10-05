var com_date_datetimefield_range={
    props:['head','search_args'],
    //data:function(){
    //    if(! this.search_args['_start_'+this.head.name]){
    //        Vue.set(this.search_args,'_start_'+this.head.name,'')
    //        var start=''
    //    }else{
    //        var start=this.search_args['_start_'+this.head.name].slice(0,10)
    //    }
    //    if(! this.search_args['_end_'+this.head.name]){
    //        Vue.set(this.search_args,'_end_'+this.head.name,'')
    //        var end=''
    //    }else{
    //        var end=this.search_args['_end_'+this.head.name].slice(0,10)
    //    }
    //    return {
    //        start:start,
    //        end:end
    //    }
    //},
    template:`<div  class="date-filter flex flex-ac">
                     <date v-model="start" :placeholder="head.label"></date>
                    <div style="display: inline-block;margin: 0 2px;" >-</div>
                        <date  v-model="end" :placeholder="head.label"></date>
                </div>`,

    computed:{
        start:{
            get:function(){
                if(this.search_args['_start_'+this.head.name]){
                    return  this.search_args['_start_'+this.head.name].slice(0,10)
                }else{
                    return ''
                }

            },
            set:function(nv){
                if(nv){
                    this.search_args['_start_'+this.head.name]=nv+' 00:00:00'
                }else{
                    this.search_args['_start_'+this.head.name]=nv
                }

            }
        },
        end:{
            get:function(){
                if(this.search_args['_end_'+this.head.name]){
                    return   this.search_args['_end_'+this.head.name] .slice(0,10)
                }else{
                    return ''
                }

            },
            set:function(nv){
                if(nv){
                    this.search_args['_end_'+this.head.name]=nv+' 23:59:59'
                }else{
                    this.search_args['_end_'+this.head.name]=nv
                }

            }
        }
    },
    //watch:{
    //    start:function(nv){
    //        if(nv){
    //            this.search_args['_start_'+this.head.name]=nv+' 00:00:00'
    //        }else{
    //            this.search_args['_start_'+this.head.name]=''
    //        }
    //    },
    //    end:function(nv){
    //        if(nv){
    //            this.search_args['_end_'+this.head.name]=nv+' 23:59:59'
    //        }else{
    //            this.search_args['_end_'+this.head.name]=''
    //        }
    //    }
    //
    //}

}
Vue.component('com-date-datetimefield-range-filter',com_date_datetimefield_range)
