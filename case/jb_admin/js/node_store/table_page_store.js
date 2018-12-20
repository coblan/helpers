var table_page_store={
    data:function(){
        return {
            tab_stack:[],
            tabs:[],
            //named_tabs:[],
            childStore_event_slot:childStore_event_slot,
        }
    },
    created:function(){
        var self=this
        // 这个不用了，转到 table_store 里面去了
        ex.each(this.childStore_event_slot,function(router){
            self.$on(router.event,function(e){
                var kws = ex.eval(router.kws,e)
                self[router.fun](kws)
            })
        })
    },
    methods:{
        hello:function(mm){
            alert(mm)
        },
        update_ctx:function(kws){
            var post_data = kws.post_data || {}
            ex.director_call(kws.director_name,post_data,function(resp){

                //Vue.set(named_ctx,router.ctx_name,resp)
                named_ctx[kws.ctx_name] = resp
            })
        },
        switch_to_tab:function(kws){
            var self=this
            var tabs=named_ctx[kws.ctx_name]
            //if(kws.named_tabs){
            //    // 传入named_tabs，造成tabs的切换
            //    var next_tabs = self.named_tabs[kws.named_tabs]
            //}else {
            //    var next_tabs = self.tabs
            //}
            self.tab_stack.push( {
                widget:'com-widget-el-tab' ,
                tabs:tabs,
                crt_tab_name:kws.tab_name,
                par_row:kws.par_row,

            })
            self.crt_row= kws.row
        },
        pop_tab_stack:function(){

            if( this.tab_stack.length != 0){
                this.tab_stack.pop()
            }
//                if(this.tab_stack.length==0){
//                    this.tabgroup.crt='_main'
//                    this.tabgroup.crt_tabs=[]
//                }
            var self=this
            Vue.nextTick(function(){
                // 返回table页面时，可能是由于布局原因，造成table看不见
                self.e_table.doLayout()
            })

        },
    }
}

window.table_page_store = table_page_store