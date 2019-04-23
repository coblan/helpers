//import { Dialog } from 'vant';
//
//Vue.use(Dialog);
import { MessageBox } from 'mint-ui';
import { Indicator } from 'mint-ui';

ex.assign(cfg,{
    fields_editor:'com-sim-fields',
    fields_local_editor:'com-sim-fields-local',
    showMsg:function(msg){
        if(typeof msg =='string'){
            //return Dialog.alert({
            //    message: msg
            //})
            return MessageBox.alert(msg)
        }else{
             //  {title:'xxx',message:'xxx'}
            //return Dialog.alert(msg)
            return MessageBox(msg)
        }
    },
    showError:function(msg){
        if(typeof msg =='string'){
            return MessageBox.alert(msg)
        }else{
            return MessageBox(msg)
        }
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
    pop_iframe:function(url,option){
       return cfg.pop_big('com-slide-iframe',{url:url,title:option.title})
    },
    show_load(){
        Indicator.open(
            {spinnerType: 'fading-circle'}
        )
    },
    hide_load(delay,msg){
        Indicator.close()
    }

})