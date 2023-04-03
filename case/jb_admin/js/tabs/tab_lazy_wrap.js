/*
* 用于封装延迟加载的tab页面
* */
var lazy_wrap={
    props:['tab_head','par_row'],
    data(){
            return {
                real_head:{}
            }
    },
    mounted(){
        if(this.tab_head.lazy_init){
            ex.eval(this.tab_head.lazy_init,{head:this.tab_head})
        }
        if(this.tab_head.lazy_director_name_express) {
            var director_name = ex.eval(this.tab_head.lazy_director_name_express, {par_row: this.par_row})
        }else {
            var director_name = ethis.tab_head.lazy_director_name
        }
        if(this.tab_head.filter_express){
            var dc = ex.eval(this.tab_head.filter_express,{par_row:this.par_row})
        }else{
            var dc = {}
        }
        ex.direction_get(director_name,dc).then(resp=>{
            debugger
            this.real_head = resp
        })
    },
    template:`<div class="com-tab-lazy-wrap">
           <component :is="real_head.editor" :ctx="real_head.ctx"></component>
</div>`
}

Vue.component('com-tab-lazy-wrap',lazy_wrap)