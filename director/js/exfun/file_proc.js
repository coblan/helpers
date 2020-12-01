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

    },
    readLocalFile({accept='',encode='utf-8'}){
        return new Promise((resolve,reject)=>{
            ex.__on_filechange=function(event){
                let files = event.target.files
                var loadCount = 0 // 已读取文件数量
                // 读取单个文件
                var out_text=''
                var loadAFile = function(file) {
                    var reader = new FileReader()
                    reader.onload = function(e) {
                        var r = this.result
                        out_text += r
                        loadCount++
                        if (loadCount == files.length) {
                            console.log('读取完毕')
                            $('#_hide_file_input').val('')
                            resolve(out_text)
                        }
                    }
                    reader.readAsText(file, encode) // 以文本形式读取

                }
                for (var i = 0; i < files.length; i++) {
                    loadAFile(files[i])
                }

            }

            if(!window._hide_file_input){
                $('body').append('<input type="file" id="_hide_file_input" style="display: none" >')
                $('#_hide_file_input').change(function(event){
                    ex.__on_filechange(event)
                })
                window._director_uploadfile_input=true
                //if(accept){
                    $('#_hide_file_input').attr('accept',accept)
                //}
                $('#_hide_file_input').click()
            }else{
                //if(accept){
                    $('#_hide_file_inputt').attr('accept',accept)
                //}
                $('#_hide_file_input').click()
            }
        })

    },
    saveLocalFile  (content, filename) {
        // 创建隐藏的可下载链接
        var eleLink = document.createElement('a');
        eleLink.download = filename;
        eleLink.style.display = 'none';
        // 字符内容转变成blob地址
        var blob = new Blob([content]);
        eleLink.href = URL.createObjectURL(blob);
        // 触发点击
        document.body.appendChild(eleLink);
        eleLink.click();
        // 然后移除
        document.body.removeChild(eleLink);
    }

}