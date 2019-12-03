export var  file_proc={
    qrcode:function(selector,kws){
            /*
            *      $("#qrcodeCanvas").qrcode({
             render : "canvas",    //设置渲染方式，有table和canvas，使用canvas方式渲染性能相对来说比较好
             text : "这是修改了官文的js文件，此时生成的二维码支持中文和LOGO",    //扫描二维码后显示的内容,可以直接填一个网址，扫描二维码后自动跳向该链接
             width : "200",               //二维码的宽度
             height : "200",              //二维码的高度
             background : "#ffffff",       //二维码的后景色
             foreground : "#000000",        //二维码的前景色
             src: '/static/images/logo.png'             //二维码中间的图片
             });
            * */
        ex.load_js_list(['/static/lib/jquery.qrcode.js','/static/lib/utf.js'],function(){
            var def_cfg = {
                render : "canvas",    //设置渲染方式，有table和canvas，使用canvas方式渲染性能相对来说比较好
                text : "",    //扫描二维码后显示的内容,可以直接填一个网址，扫描二维码后自动跳向该链接
                width : "200",               //二维码的宽度
                height : "200",              //二维码的高度
                background : "#ffffff",       //二维码的后景色
                foreground : "#000000",        //二维码的前景色
                src: ''             //二维码中间的图片
            }

            ex.assign(def_cfg,kws)
            $(selector).qrcode(def_cfg);
        })
    },
    uploads:function (files,url,success,progress) {
        var url= url ||'/d/upload?path=general_upload/images'
        var fd = new FormData();
        for(var x=0;x<files.length;x++){
            var file=files[x]
            fd.append(file.name,file);
        }
        return new Promise(function(resolve,reject){
            $.ajax({
                url:url,
                type:'post',
                data:fd,
                contentType: false,
                success:function(resp){
                    resolve(resp)
                    if(success){
                        success(resp)
                    }
                } ,
                processData:false,
                xhr:function() {
                    var xhr = new window.XMLHttpRequest();
                    xhr.upload.addEventListener("progress", function(evt) {
                        if (progress &&evt.lengthComputable) {
                            var percentComplete = evt.loaded / evt.total;
                            progress(percentComplete)
                            //console.log('进度', percentComplete);
                        }
                    }, false);

                    return xhr;
                }
            })



        })

    }
}