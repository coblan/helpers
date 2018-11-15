
export var network ={
    get:function(url,callback){
        //replace $.get
        var self=this
        var wrap_callback=function (resp) {
            if (resp.msg) {
                self.show_msg(resp.msg)
            }
            if (resp.status && typeof resp.status == 'string' && resp.status != 'success') {
                cfg.hide_load()
                return
            } else {
                callback(resp)
            }
        }
        return $.get(url,wrap_callback)
    },
    post:function(url,data,callback){
        var self=this
        var wrap_callback=function (resp) {
            var msg = []
            if(resp.msg ){
                if(typeof resp.msg == 'string'){
                    msg.push(resp.msg)
                }else{
                    msg = msg.concat(resp.msg)
                }
            }
            for(var k in resp){
                if(resp[k] && resp[k].msg){
                    if(typeof resp[k].msg == 'string'){
                        msg.push(resp[k].msg)
                    }else {
                        msg=msg.concat(resp[k].msg)
                    }
                }
            }
            if(msg.length!=0){
                if(resp.success===false){
                    cfg.warning(msg.join('\n'))
                }else{
                    cfg.showMsg(msg.join('\n'))
                }
            }
            //if (resp.status && typeof resp.status == 'string' && resp.status != 'success') {
            if (resp.success === false) {
                cfg.hide_load() // sometime
                return
            } else {
                callback(resp)
            }
        }
        return $.post(url,data,wrap_callback)
    },
    load_js: function(src,success) {
        success = success || function(){};
        var name = src //btoa(src)
        if(!window['__js_hook_'+name]){
            window['__js_hook_'+name]=[]
        }
        window['__js_hook_'+name].push(success)
        var hooks=window['__js_hook_'+name]
        if(window['__js_loaded_'+name]){
            while (hooks.length>0){
                hooks.pop()()
            }
        }
        if(! window['__js_'+name]){
            window['__js_'+name]=true
            var domScript = document.createElement('script');
            domScript.src = src;

            domScript.onload = domScript.onreadystatechange = function() {
                if (!this.readyState || 'loaded' === this.readyState || 'complete' === this.readyState) {
                    window['__js_loaded_'+name]=true
                    while (hooks.length>0){
                        hooks.pop()()
                    }
                    this.onload = this.onreadystatechange = null;
                    // 让script元素显示出来
                    //this.parentNode.removeChild(this);
                }
            }
            document.getElementsByTagName('head')[0].appendChild(domScript);
        }
    },
    load_js_list:function(js_list,success){
        var length = js_list.length
        ex.each(js_list,function(js){
            ex.load_js(js,function(){
                length -=1
                if(length ==0){
                    success()
                }
            })

        })
    },
    load_css:function (src) {
        var name = btoa(src)
        if(window['__src_'+name]){
            return
        }
        window['__src_'+name]=true
        $('head').append('<link rel="stylesheet" href="'+src+'" type="text/css" />')
    },
    director_call:function(director_name,kws,callback){
        var post_data=[{fun:"director_call",director_name:director_name,kws:kws}]
        ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
            callback( resp.director_call )
        })
    },

    download:function(strPath){
            var varExt = strPath.split('.');
            //alert(varExt.length);
            if (varExt[varExt.length - 1] == "txt") {
                window.open(strPath);
            }
            else {
                var iframe;
                iframe = document.getElementById("hiddenDownloader");
                if (iframe == null) {
                    iframe = document.createElement('iframe');
                    iframe.id = "hiddenDownloader";
                    iframe.style.visibility = 'hidden';
                    document.body.appendChild(iframe);
                }
                iframe.src = strPath;
            }
            return false;
    }
}