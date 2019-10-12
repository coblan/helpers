/*
* 用于封装延迟加载的tab页面
* */
var lazy_wrap={
    props:['tab_head','par_row'],

    mounted(){
        if(this.tab_head.lazy_init){
            ex.eval(this.tab_head.lazy_init,{head:this.tab_head})
        }
    },
    template:`<div class="com-tab-lazy-wrap">
    </div>`
}

Vue.component('com-tab-lazy-wrap',lazy_wrap)