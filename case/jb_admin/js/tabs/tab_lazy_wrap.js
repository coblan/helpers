/*
* 用于封装延迟加载的tab页面
* */
var lazy_wrap={
    props:['tab_head','par_row'],
    data(){
            return {
                real_head:{},
                loaded:false,
            }
    },
    mounted(){

        if(this.tab_head.mounted_express){
            ex.eval(this.tab_head.mounted_express,{head:this.tab_head,vc:this})
        }else{

            if(this.tab_head.lazy_init){
                ex.eval(this.tab_head.lazy_init,{head:this.tab_head})
            }


            if(this.tab_head.lazy_director_name_express) {
                var director_name = ex.eval(this.tab_head.lazy_director_name_express, {par_row: this.par_row})
            }else {
                var director_name = this.tab_head.lazy_director_name
            }
            if(this.tab_head.filter_express){
                var filter_dc = ex.eval(this.tab_head.filter_express,{par_row:this.par_row})
            }else{
                var filter_dc = {}
            }

            ex.director_get(director_name,filter_dc).then(resp=>{
                this.real_head = resp
                this.loaded=true
            })


        }



        // ex.director(director_name).call("get_head_context",filter_dc).then(resp=>{
        //     this.real_head = {
        //         tab_head: resp
        //     }
        // })
    },
    template:`<div class="com-tab-lazy-wrap">
           <component v-if="loaded" :is="real_head.editor" :tab_head="real_head.tab_head" :par_row="par_row"></component>
</div>`
}

Vue.component('com-tab-lazy-wrap',lazy_wrap)