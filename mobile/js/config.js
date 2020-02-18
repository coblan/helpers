//import { Dialog } from 'vant';
//
//Vue.use(Dialog);
//import { MessageBox } from 'mint-ui';
//import { Indicator } from 'mint-ui';
require('./styl/config.styl')

// 下面的代码是为了解决移动端，ios浏览器 100vh包含navbar的高度，造成无法定位foot吸底问题。
// 原理是声明一个css变量，--app-height 来记录 window.innerHeight,用它替代 100vh
// https://stackoverflow.com/questions/37112218/css3-100vh-not-constant-in-mobile-browser
const appHeight = () => {
    const doc = document.documentElement

    //doc.style.setProperty('--app-height', `${window.innerHeight}px`)
    doc.style.setProperty('--app-height', $('#main-panel').height()+'px')
    doc.style.setProperty('--app-width',$('#main-panel').width()+'px')
}
window.addEventListener('resize', appHeight)
//appHeight()
ex.assign(cfg,{
    updateSizeConfig(){
        appHeight()
    }
})

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
            cfg.hide_load()
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
        return MINT.Indicator.open({spinnerType: 'fading-circle'})
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
        }else if(delay){
            cfg.toast('操作成功！')
        }
    },
    toast(msg){
        return MINT.Toast(msg)
        //MINT.Toast({duration:10000,message:'sdgdsggg'})
        //vant.Toast(msg,{zIndex:999999});
    },
    toast_success(msg){
        vant.Toast.success(msg)
    },
    open_image(imgsrc){
        vant.ImagePreview({
                images:[imgsrc],
                startPosition: 0,
            }
        );
    }
})

//$(window).resize(function(){
//    debugger
//    $('.dyn-resize').each(function(){
//        debugger
//        var size_express = $(this).attr('data-size-express')
//        var sizestr = ex.eval(size_express,{winheight:window.innerHeight,ele:$(this) })
//        $(this).css(sizestr)
//
//    })
//})

//window.onbeforeunload = function() {
//
//    alert('退出页面')
//}