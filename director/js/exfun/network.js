
import {hook_ajax_msg,hook_ajax_csrf,show_upload,hide_upload} from './network/ajax_fun.js'

hook_ajax_msg()
hook_ajax_csrf()

export var network ={
    get:function(url,callback){
        //replace $.get
        var self=this
        if(callback){
            return $.get(url,callback)
        }else{
            return new Promise((resolve,reject)=>{
                $.get(url,(resp)=>{
                    resolve(resp)
                })
            })
        }
        //var wrap_callback=function (resp) {
        //    if (resp.msg) {
        //        self.show_msg(resp.msg)
        //    }
        //    if (resp.status && typeof resp.status == 'string' && resp.status != 'success') {
        //        cfg.hide_load()
        //        return
        //    } else {
        //        callback(resp)
        //    }
        //}
        //return $.get(url,wrap_callback)
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
            // 业务逻辑里面的msg 由正常函数去处理
            //for(var k in resp){
            //    if(resp[k] && resp[k].msg){
            //        if(typeof resp[k].msg == 'string'){
            //            msg.push(resp[k].msg)
            //        }else {
            //            msg=msg.concat(resp[k].msg)
            //        }
            //    }
            //}

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
                }
                // 业务逻辑里面的msg 由正常函数去处理
                //else{
                //    cfg.showMsg(msg.join('\n'))
                //}
            }


        }
        if(typeof data == "object"){
            data = JSON.stringify(data)
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
        return new Promise( (resolve,reject)=>{
            var length = js_list.length
            ex.each(js_list,function(js){
                ex.load_js(js,function(){
                    length -=1
                    if(length ==0){
                        if(success){
                            success()
                        }
                        resolve()
                    }
                })

            })
        })

    },
    load_css:function (src) {
        var name = btoa(src)
        if(window['__src_'+name]){
            return
        }
        window['__src_'+name]=true
        var domScript = document.createElement('link');
        domScript.href = src;
        domScript.type='text/css'
        domScript.rel='stylesheet'
        document.getElementsByTagName('head')[0].appendChild(domScript);

        //$('head').append('<link rel="stylesheet" href="'+src+'" type="text/css" />')
    },
    append_css:function(style){
        if(!window.md5){
            var pro = ex.load_js('https://cdn.jsdelivr.net/npm/blueimp-md5@2.10.0/js/md5.min.js')
        }else{
            var pro = 1
        }
        Promise.all([pro]).then(()=>{
                let key = md5(style)
                if(!window['__css_'+key]){
                    $("<style type='text/css'> "+style + " </style>").appendTo("head");
                    window['__css_'+key]=true
                }
        })

    },
    load_image(url) {
        var img = new Image();
        img.src = url;

        var p = new Promise(function(resolve,reject){
            if(img.complete) {
                //接下来可以使用图片了
                //do something here
                resolve()
            }
            else {
                img.onload = function() {
                    //接下来可以使用图片了
                    //do something here
                    resolve()
                };
            }
        })
        return p
    },
    director_call:function(director_name,kws,callback){
        //var post_data=[{fun:"director_call",director_name:director_name,kws:kws}]
        if(ex.isEmpty(kws)){
            var post_data = {}
        }else{
            var post_data= JSON.stringify(kws)
        }
        if (callback && typeof callback =='object'){
            var option = callback
        }else{
            var option ={}
        }
        if(option.catch ){
            window._director_catch =  window._director_catch || {}
            var key = md5(director_name+JSON.stringify(kws))

            if(window._director_catch[key]){
                var catch_value = window._director_catch[key]
                if(Array.isArray( catch_value) && typeof catch_value[0] =='function' ){
                    // 表示前面的请求还在进行中
                    return new Promise((resolve,reject)=>{
                        catch_value.push((resp)=>{
                            resolve(resp)
                        })
                    })
                }else{
                    return Promise.resolve(catch_value)
                }
            }else {
                // 第一个 请求 放个空函数，触发后面的 往 catch里面 插入 function
                window._director_catch[key] = [()=>{}]
            }
        }
        if(callback && typeof callback=='function'){
            //ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
            //    callback( resp.director_call )
            //})
            ex.post('/dapi/'+director_name,post_data,function(resp){
                if(resp.success){
                    callback( resp.data )
                }

            })
        }else{
            var post_url = '/dapi/'+director_name
            if(option.transaction != undefined){
                post_url = ex.appendSearch(post_url,{transaction:option.transaction})
            }
            return new Promise(function(resolve,reject){
                    //ex.post('/d/ajax',JSON.stringify(post_data)).then(
                    //    function(resp){
                    //        resolve(resp.director_call)
                    //    }
                    //)
                ex.post(post_url,post_data).then(
                    function(resp){
                        if(resp.success) {
                            if(resp._question){
                                ex.eval(resp._question,{director_name:director_name,kws:kws,resolve:resolve})
                            }else{
                                resolve(resp.data)
                                // 缓存代码
                                if(option.catch ){
                                    var catch_value = window._director_catch[key]
                                    if(Array.isArray( catch_value) && typeof catch_value[0] =='function' ){
                                        ex.each( window._director_catch[key],func=>{
                                            func(resp.data)
                                        })
                                    }
                                    window._director_catch[key] = resp.data
                                }
                            }
                        }
                    }
                )

            })
        }

    },
    director(director_name){
        // 为了兼容性，暂时屏蔽 Proxy 版本的代码
        //let handler = {
        //    get: function(target, attr_name){
        //        return function (kws){
        //            if(kws == undefined){
        //                kws = {}
        //            }
        //            return ex.director_call('d.director_element_call',{director_name:director_name,attr_name:attr_name,kws:kws})
        //        }
        //    }
        //};
        //return new Proxy({},handler)

        return {
            call(methed,kws){
                  if(kws == undefined){
                       kws = {}
                   }
                 return ex.director_call('d.director_element_call',{director_name:director_name,attr_name:methed,kws:kws})
            }
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
    },
    uploadfile({url,accept}={}){
        this.__upload_url =url
        return new Promise((resolve,reject)=>{
            ex.__on_filechange=function(event){
                let new_selected_files = event.target.files
                var up_url = ex.__upload_url || '/d/upload?path=general_upload&split=date'
                cfg.show_load()
                ex.uploads(new_selected_files,up_url,function(url_list){
                    cfg.hide_load()
                    $('#__director-upload-file-input').val('')
                    resolve(url_list)
                })
            }

            if(!window._director_uploadfile_input){
                $('body').append('<input type="file" id="__director-upload-file-input" style="display: none" >')
                $('#__director-upload-file-input').change(function(event){
                    ex.__on_filechange(event)
                })
                window._director_uploadfile_input=true
                if(accept){
                    $('#__director-upload-file-input').attr('accept',accept)
                }
                $('#__director-upload-file-input').click()
            }else{
                if(accept){
                    $('#__director-upload-file-input').attr('accept',accept)
                }
                $('#__director-upload-file-input').click()
            }

        })
    },
    refresh_row(row){
        return ex.director_call(row._director_name,{pk:row.pk}).then(resp=>{
            ex.vueAssign(row,resp.row)
        })
    }
}