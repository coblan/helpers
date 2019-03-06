window.cfg={
    env:{
        width:$(window).width(),
        height:$(window).height(),
    },
    showMsg:function(msg){
        layer.alert(msg);
    },
    warning:function(msg){
        layer.alert(msg,{title:['提示','color:white;background-color:#f0ad4e'],icon: 5})
    },
    showError:function(msg){
        layer.alert(msg, {icon: 5,title:'错误'});
    },
    showTip:function(msg,...parm){
        layer.msg(msg,...parm)
    },
    tr:{
        'picture_size_excceed':'图片尺寸不能超过{maxsize}'
    },
    show_load:function(){
        this._loader_index = layer.load(1)
    },
    hide_load:function(delay,msg){
        layer.close(this._loader_index)
        if(delay){
            var realMsg = msg || '操作成功'
            layer.msg(realMsg,{time:delay})
        }
    },
    pop_edit:function(fields_ctx){

    },
    pop_edit_local:function(fields_ctx,callback){
        var winindex = pop_edit_local(fields_ctx.row,fields_ctx,callback)
        return function (){
            layer.close(winindex)
        }
    },

    pop_big:function(editor,ctx,callback){
        var width = Math.min(cfg.env.width*0.9,950)
        var heigth = Math.min(cfg.env.height*0.9,700)
        var winindex = pop_layer(ctx,editor,callback,{
            area: [width+'px', heigth+'px'],
        })
        return function (){
            layer.close(winindex)
        }
    },
    pop_middle:function(editor,ctx,callback){
        var width = Math.min(800,cfg.env.width)
        var layercfg={
            area: [width+'px', '500px'],
        }
        if(ctx.layer){
            ex.assign(layercfg,ctx.layer)
        }

        var winindex = pop_layer(ctx,editor,callback,layercfg)
        return function (){
            layer.close(winindex)
        }
        //store.commit('left_in_page',{editor:editor,ctx:ctx,callback:callback})
        //return function (){
        //    history.back()
        //}
    },
    pop_small:function(editor,ctx,callback){
        //return pop_mobile_win(editor,ctx,callback)
        var layer_cfg={
            title:ctx.title || '详细',
            area:ctx.area || ['42rem','32rem']
        }
        if(ctx.layer){
            ex.assign(layer_cfg,ctx.layer)
        }
        var winindex = pop_layer(ctx,editor,callback,layer_cfg)
        return function (){
            layer.close(winindex)
        }
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
        var dc = {
            type: 2,
            title:'',
            area: ['80%', '80%'],
            content: url //这里content是一个URL，如果你不想让iframe出现滚动条，你还可以content: ['http://sentsin.com', 'no']
        }
        ex.assign(dc,option)
        layer.open(dc);
    },
}

$(window).resize(function(){
    cfg.env.width=$(window).width()
    cfg.env.height=$(window).height()
})