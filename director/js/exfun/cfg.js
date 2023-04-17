
require('./scss/cfg.scss')
// require('weblib/style')
// require('weblib/pc/style')
import * as web_style from 'weblib/style'
import * as pc_style from 'weblib/pc/style'
import {pop_layer} from './cfg/pop_layer.js'

$(document).ready(function () { }).keydown(
    function (e) {

        if (e.which === 27) {
            if(cfg.layer_index_stack.length>0){
                layer.close(cfg.layer_index_stack[cfg.layer_index_stack.length-1]);
            }
        }
    });

var cfg={
    ui_editor: {},
    bus:new Vue(),
    layer_index_stack:[],
    env:{
        width:$(window).width(),
        height:$(window).height(),
    },
    scrollTo({selector,url,top=0}){
        // if(url){location.path = url}

        var real_top = document.querySelector(selector).offsetTop +top
        // document.documentElement.scrollTop=top
        document.documentElement.scrollTo({ top: real_top, behavior: 'smooth' })
    },
    prompt(mycfg){
        //{
        //    formType: 2,
        //        value: '初始值',
        //    title: '请输入值',
        //    area: ['800px', '350px'] //自定义文本域宽高
        //}
        mycfg = mycfg || {}
        return new Promise(function(resolve,reject){
            layer.prompt(mycfg,function(val, index){
                resolve(val)
                layer.close(index);
            });
        })
    },
    showMsg:function(msg,options){

        return new Promise((resolve,reject)=>{
            if(options){
                layer.alert(msg,options,function(index){
                    //do something
                    layer.close(index);
                    resolve()
                });
            }else{
                layer.alert(msg,function(index){
                    //do something
                    layer.close(index);
                    resolve()
                });
            }

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
    //tr:{
    //    'picture_size_excceed':'图片大小不能超过{maxsize}'
    //},
    tr(wd){
        return js_config.tr[wd] || wd
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
    pop_vue_com:function(editor,ctx,option){
        return new Promise(function(resolve,reject){
            var callback = function(e){
                close_fun()
                // 用户点击layer的叉叉退出弹出框时,e==__end_by_user
                if(e != '__end_by_user'){
                    resolve(e)
                }else{
                    console.log('user x close win, in promise condition,get reject, if not try catch may get error')
                    reject()
                }
            }
            ctx.ops_loc = ctx.ops_loc || 'bottom'
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
            var index =layer.confirm(msg,
                {icon: 3,
                    title:cfg.tr('确认'),
                    btn: [cfg.tr("确定"), cfg.tr("取消")],
                    end:function(){
                        ex.remove(cfg.layer_index_stack,index)
                        }
            }, function(index){
                layer.close(index);
                resolve()
            },function(index){
                    layer.close(index);
                    reject()
                });

            cfg.layer_index_stack.push(index);
        })
    },
    select(msg,actions,option){
        var index=0
        var btns= ex.map(actions,action=>{return action.label})
        var funclist= ex.map(actions,action=>{return (function(){ ex.eval(action.action,{index:index,option:option})  })})
        index = layer.confirm(msg, {
            btn: btns ,//按钮
            end:function(){
                ex.remove(cfg.layer_index_stack,index)
            }
        },...funclist);
        cfg.layer_index_stack.push(index);
    },
    _tab_call_back:[],
    switch_to_tab(kws){
        // 从 table_page_store 移过来的。因为 live_table 可能有这个需求
        var self=this
        var tabs=named_ctx[kws.ctx_name]
        if(!tabs){
            throw `named_ctx.${kws.ctx_name} 不存在，检查是否传入`
        }

        var canfind = ex.findone(tabs,{name:kws.tab_name})
        if(!kws.tab_name || !canfind ){
            kws.tab_name = tabs[0].name
        }
        if(window.root_live){
            // keeplive 页面
            root_live.open_live(live_el_tab,{tabs:tabs,
                title:kws.par_row._label,
                crt_tab_name:kws.tab_name,
                par_row:kws.par_row,
                type:kws.type,
                top_editor: kws.top_editor,
                top_ctx: kws.top_ctx,
                last_ps:kws.last_ps,
                genVc:kws.genVc})
        }else{
            // 这个应该是用在 table_new.html中的
            root_store.$emit('switch-to-tab',{
                widget:'com-widget-el-tab' ,
                tabs:tabs,
                crt_tab_name:kws.tab_name,
                par_row:kws.par_row,
                type:kws.type,
                top_editor: kws.top_editor,
                top_ctx: kws.top_ctx,
                genVc:kws.genVc
            })
        }
        return new Promise((resolve,reject)=>{
            this._tab_call_back.push(()=>{
                resolve()
            })
        })


    },
    switch_back(){
        // 这里很混乱，root_live只存在于live.html中，而live_root存在于live.html和table_new.html中
        if(window.root_live){
            var com = window.live_root.stack.pop()
            Vue.delete(window.live_root.$options.components,com)
        }else{
            window.live_root.childStore.tab_stack.pop()
        }
    }
}

$(window).resize(function(){
    cfg.env.width=$(window).width()
    cfg.env.height=$(window).height()
})

function assign(dst,src) {
    for(var key in src){
        dst[key]=src[key]
    }
    return dst
}

import {notify} from  './config/notify'
assign(cfg,notify)

window.cfg=cfg