ex.assign(cfg,{
    pop_big:function(editor,ctx,callback){
        store.commit('left_in_page',{editor:editor,ctx:ctx,callback:callback})
        return function (){
            history.back()
        }
    },
    pop_middle:function(editor,ctx,callback){
       return pop_mobile_win(editor,ctx,callback)
    },
    pop_small:function(editor,ctx,callback){
        return pop_mobile_win(editor,ctx,callback)
        //pop_layer(ctx,editor,callback)
    },
    close_win:function(index){
        if(index=='full_win'){
            history.back()
        }
    },
    pop_close:function(close_func){
        // 关闭窗口，窗口创建函数返回的，全部是一个关闭函数
        close_func()
    },
    pop_iframe:function(url,option){
        this.pop_big('com-slide-iframe',{url:url,title:option.title})
    },

})