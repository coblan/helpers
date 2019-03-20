
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
        if(callback){
            ex._post(url,data,callback)
        }else{
            var p = new Promise(function(resolve,reject){
                ex._post(url,data,function(resp){
                    resolve(resp)
                })
            })
            return p
        }
    },
    _post:function(url,data,callback){
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

            var success=true
            if(resp.success ==false ){
                success = false
            }
            if(resp.status && typeof resp.status == 'string' && resp.status != 'success'){
                success = false
            }
            //if(! success){
            //    hide_upload(300)
            //    if(resp.msg){
            //        cfg.showError(resp.msg)
            //    }
            //}else{
            //    if(resp.msg){
            //        cfg.showMsg(resp.msg)
            //    }
            //    callback(resp)
            //}

            //if (resp.status && typeof resp.status == 'string' && resp.status != 'success') {
            if (!success) {
                cfg.hide_load() // sometime
            } else {
                var rt = callback(resp)
                if(rt==false){
                    return  // 模拟事件冒泡，返回false，就不继续执行下面的语句了。
                }
            }

            if(msg.length!=0){
                if(!success){
                    cfg.showError(msg.join('\n'))
                }else{
                    cfg.showMsg(msg.join('\n'))
                }
            }


        }
        return $.post(url,data,wrap_callback)
    },
    load_js:function(src,success){
        if(success){
            return ex._load_js(src,success)
        }else{
            var p = new Promise(function(resolve,reject){
                ex._load_js(src,function(){
                    resolve()
                })
            })
            return p
        }
    },
    _load_js: function(src,success) {
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
    append_css:function(style){
        let key = md5(style)
        if(!window['__css_'+key]){
            $("<style type='text/css'> "+style + " </style>").appendTo("head");
        }
    },
    director_call:function(director_name,kws,callback){
        var post_data=[{fun:"director_call",director_name:director_name,kws:kws}]
        if(callback){
            ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                callback( resp.director_call )
            })
        }else{
            return new Promise(function(resolve,reject){
                    ex.post('/d/ajax',JSON.stringify(post_data)).then(
                        function(resp){
                            resolve(resp.director_call)
                        }
                    )
            })
        }

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