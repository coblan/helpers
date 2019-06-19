require('./scss/cfg.scss')

window.cfg={
    env:{
        width:$(window).width(),
        height:$(window).height(),
    },
    showMsg:function(msg){
        return new Promise((resolve,reject)=>{
            layer.alert(msg,function(index){
                //do something
                layer.close(index);
                resolve()
            });
        })

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
    toast(msg,...parm){
        layer.msg(msg,...parm)
    },
    tr:{
        'picture_size_excceed':'图片大小不能超过{maxsize}'
    },

    show_cloak:function(){
        this._cloak_index = layer.load()
    },
    hide_cloak:function(){
        layer.close(this._cloak_index)
    },
    show_load:function(msg){
        if(msg){
            this._loader_index =layer.msg(msg, {
                icon: 16
                ,shade: 0.01,
                time:0
            });
        }else{
            this._loader_index = layer.load(1)
        }
    },
    hide_load:function(delay,msg){
        if(! this._loader_index){
            return
        }
        layer.close(this._loader_index)
        this._loader_index =null
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
    pop_vue_com:function({ctx,editor,option}){
        return new Promise(function(resolve,reject){
            var callback = function(e){
                close_fun()
                resolve(e)
            }
            var winindex = pop_layer(ctx,editor,callback,option)
            var close_fun = function (){
                layer.close(winindex)
            }
        })
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
    confirm:function(msg){
        return new Promise(function(resolve,reject){
            layer.confirm(msg, {icon: 3, title:'提示'}, function(index){
                layer.close(index);
                resolve()
            });
        })
    }
}

$(window).resize(function(){
    cfg.env.width=$(window).width()
    cfg.env.height=$(window).height()
})