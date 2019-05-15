//import { Dialog } from 'vant';
//
//Vue.use(Dialog);
//import { MessageBox } from 'mint-ui';
//import { Indicator } from 'mint-ui';
require('./styl/config.styl')

ex.assign(cfg,{
    fields_editor:'com-sim-fields',
    fields_local_editor:'com-sim-fields-local',
    showMsg:function(msg){
        if(typeof msg =='string'){
            //return Dialog.alert({
            //    message: msg
            //})
            return MINT.MessageBox.alert(msg)
        }else{
             //  {title:'xxx',message:'xxx'}
            //return Dialog.alert(msg)
            return MINT.MessageBox(msg)
        }
    },
    showError:function(msg){
        if(typeof msg =='string'){
            return MINT.MessageBox.alert(msg)
        }else{
            return MINT.MessageBox(msg)
        }
    },
    confirm(msg){
        return MINT.MessageBox.confirm(msg)
    },
    pop_edit_local:function(ctx,callback){
        ctx.fields_editor='com-sim-fields-local'
        return cfg.pop_big('com-fields-panel',ctx,callback)
    },
    pop_big:function(editor,ctx,callback){
        slide_mobile_win({editor:editor,ctx:ctx,callback:callback})
        //window.slide_win.left_in_page({editor:editor,ctx:ctx,callback:callback})
        return function (){
            history.back()
        }
    },
    pop_middle:function(editor,ctx,callback){
        slide_mobile_win({editor:editor,ctx:ctx,callback:callback})
        //window.slide_win.left_in_page({editor:editor,ctx:ctx,callback:callback})
        return function (){
            history.back()
        }
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
    //slideIn(editor,ctx){
    //   return new Promise((resolve,reject)=>{
    //       function callback(e){
    //           resolve(e,close_fun)
    //       }
    //        var close_fun = cfg.pop_big(editor,ctx,callback)
    //    })
    //},
    pop_iframe:function(url,option){
       return cfg.pop_big('com-slide-iframe',{url:url,title:option.title})
    },
    show_load(){
        MINT.Indicator.open({spinnerType: 'fading-circle'})
        //vant.Toast.loading({
        //    mask: true,
        //    message: '加载中...',
        //    duration: 0,
        //});
    },
    hide_load(delay,msg){
        //vant.Toast.clear()
        MINT.Indicator.close()
        if(msg){
            cfg.toast(msg)
        }
    },
    toast(msg){
        MINT.Toast(msg)
        //MINT.Toast({duration:10000,message:'sdgdsggg'})
        //vant.Toast(msg,{zIndex:999999});
    }

})