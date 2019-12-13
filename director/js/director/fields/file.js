/*
>>>front/file.rst>
===========
文件上传
===========

主要内容
========
fl
    包含可以操作file对象的函数，例如上传upload,批量上传uploads.

file-input
    该组件用户收集用户输入。只能返回file list 。所以，如果使用upload上传文件，必须取 [0] 第一个file对象。

img-uploador
    图片选择，自动上传。

多个文件上传步骤
==============

1. Vue.data设置::

    data:{
    files:[],
    },

2. 在html中插入Vue组件::

    <file-input id='jjyy' v-model='files' multiple></file-input>

3. 在Methods中上传::

    fl.uploads(files,url,function(resp){  // url 可以忽略，默认url为 /face/upload
        resp ....
    })

单个文件
=======
1.Vue.data设置::

    data:{
        files:[],
    },

2. 在html中插入Vue组件::

    <file-input id='jjyy' v-model='files'></file-input>

3. 在Methods中上传::

     fl.uploads(this.files[0],url,function(resp){
        resp ....
     })

.. Note:: 默认上传url是/face/upload ，该接口返回的是 file_url_list。

上传进度
=========
进度只是上传进度，判断文件是否被后端接收成功，需要判断是否success回调被调用::

     fl.upload(this.file2[0],'/face/upload',function(url_list){

     },function(progress){
        console.log(progress)
     })

预览图片
=========
从file-input读出数据，然后赋予图片的src ::

    f1.read(this.files[0],function (data) {
            $('#haha')[0].src = data
    }


上传图片
==========
::

    <img-uploador v-model='xxx_url_variable'></img-uploador>   //默认上传，使用的是 fl.upload默认地址 /face/upload
    <img-uploador v-model='xxx_url_variable' up_url='xxx'></img-uploador>

具备裁剪性质::

    <img-uploader v-model='xxx' :config='{crop:true,aspectRatio: 8 / 10}'></img-uploader>


样式技巧
========
1. 自定义样式

    <file-inpu>不支持直接自定义样式。但是可以通过其他方式自定义。最简单的方式是：

    * 隐藏<file-input> ，
    * 然后触发其click事件('.file-input').click()
<<<<
*/



require('./scss/file.scss')


var fl={
	read:function (file,callback) {
        // 读完文件后，调用callback
		var reader = new FileReader();
    	reader.onloadend = function () {
	        // 图片的 base64 格式, 可以直接当成 img 的 src 属性值
	        var dataURL = reader.result;
	        //var img = new Image();
	        //img.src = dataURL;
	        // 插入到 DOM 中预览
	        //$('#haha')[0].src=dataURL
	        callback(dataURL) 
	    };
	    reader.readAsDataURL(file); // 读出 base64
	},
	upload:function (file,url,success,progress) {
            if(ex.is_fun(url)){
                var progress = success
                var success = url
                var url='/d/upload'
            }else{
                var url=url||'/d/upload'
            }

            var fd = new FormData();
            fd.append('file',file);
            $.ajax({
                url:url,
                type:'post',
                data:fd,
                contentType: false,
                success:success,
                //success:function (data) {
                //    success(data)
                //},
                processData:false, 
		       xhr:function() {
			        var xhr = new window.XMLHttpRequest();
			        xhr.upload.addEventListener("progress", function(evt) {
			            if (progress && evt.lengthComputable) {
			                var percentComplete = evt.loaded / evt.total;
                            progress(percentComplete)
			                //console.log('进度', percentComplete);
			            }
			        }, false);

			        return xhr;
			}
		})
	},
	uploads:function (files,url,success,progress) {
            if(ex.is_fun(url)){
                var progress = success
                var success = url
                var url='/d/upload'
            }else{
                var url=url||'/d/upload'
            }

        	var fd = new FormData();
        	for(var x=0;x<files.length;x++){
	        	var file=files[x]
	        	 fd.append(file.name,file);
        	}
            $.ajax({
                url:url,
                type:'post',
                data:fd,
                contentType: false,
                success:success,
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
        }
}

var file_input= {
    template: "<input class='file-input' type='file' @change='on_change($event)'>",
    props: ['value','name'],
    data: function () {
        return {
            files: []
        }
    },
    watch: {
        value: function (v) {
            // when input clear selected file, Component file-input need clear too.
            // Brower prohebit to set to Un-none string
            if (v == '') {
                $(this.$el).val('')
                //this.$el.value = v
            }
        }
        ,
    },
    methods: {
        on_change: function (event) {
            this.files = event.target.files
            this.$emit('input', this.files)
        },
        clear:function(){
            $(this.$el).val('')
        }
    }
}

Vue.component('file-input',file_input)


/*
<img-uploader v-model='xxx'></img-uploader>
 <img-uploader v-model='xxx' :config='{crop:true,aspectRatio: 8 / 10}'></img-uploader>

 accept='image/gif,image/jpeg,image/png'
*/

var img_uploader={
    props:['value','up_url','config'],
    data:function(){
        return {
            img_files:'',
            url:this.value,
            disable:false,
        }
    },
    computed:{
        cfg:function(){
            var dc ={
                crop:false,
                crop_config:{}
            }
            if(this.config){
                ex.assign(dc,this.config)
            }
            return dc
        },
        crop_config:function(){
            // 用cfg来代表内部设置，本来不应该有这个属性了，但是没弄清楚，以后来整个这个属性。
            if(this.config && this.config.crop){
                var temp_config=ex.copy(this.config)
                delete temp_config.crop
                return temp_config
            }else{
                return {}
            }
        },
        rotate_str(){
            return  'rotate('+ex.parseSearch(this.url).rotate || 0+ 'deg)'
        }
    },

    template:`
          <div :class='["up_wrap logo-input img-uploader",{"disable":disable}]'>
            <file-input v-if="!cfg.crop"
                ref="file_input"
                accept='image/*'
                v-model= 'img_files'>
            </file-input>
            <!--<img-crop class='input' v-if='cfg.crop' v-model='img_files' :config="crop_config">-->
            <!--</img-crop>-->
            <div style="padding: 40px" @click="select()">
                <a class='choose'>Choose</a>
            </div>
            <div v-if='url' class="closeDiv">
                <div class="close" @click='clear()'>
                    <i class="fa fa-times-circle" aria-hidden="true" style="color:red;position:relative;left:30px;"></i>
                </div>
                <div class="close" v-if="cfg.can_edit" @click="edit()">
                    <i class="fa fa-edit" aria-hidden="true" style="color:black;position:relative;left:30px;top:30px"></i>
                </div>

                <img :src="url" alt="" class="logoImg">
            </div>
             <div class="close" v-if="cfg.can_input" @click="do_input()">
                <i class="fa fa-edit" aria-hidden="true" style="color:black;position:relative;left:30px;top:30px"></i>
            </div>
            </div>
        `,
    watch:{
        value:function(v){
          this.url=v
        },
        img_files:function(v){
            var self=this
            console.log('start upload')
            if(v==""){
                return
            }
            Promise.resolve().then(()=>{
                if(self.cfg.first_edit){
                    return cfg.pop_vue_com('com-image-crop',{file:v[0]},{
                        title:false,
                        area: ['90%', '90%'],
                        shade: 0.8,
                        skin: 'img-shower',
                        shadeClose: true,
                    })
                }else{
                    return v[0]
                }
            }).then((file1)=>{
                if(! self.validate(file1)){
                    return Promise.reject()
                }
                if(self.cfg.maxspan){
                    return compressImage(file1,self.cfg.maxspan,0)
                }else{
                    return file1
                }
            }).then((file1)=>{
                var files = [file1]
                ex.uploads(files,this.up_url).then((url_list)=>{
                    self.url=url_list[0]
                    self.$emit('input',self.url)
                    self.$emit('select')
                })
            }).catch(()=>{
                this.clear()
            })
        }
    },
    methods:{
        read_image(img_url){
            var request = new XMLHttpRequest();
            request.open('GET', img_url, true);
            request.responseType = 'blob';
            return new  Promise((resolve,reject)=>{
                request.onload = function() {
                    resolve(request.response)
                };
                request.send();
            })
        },
        do_input(){
            cfg.prompt({value:this.url}).then((val)=>{
                this.url = val
                this.$emit('input',this.url)
                this.$emit('select')
            })
        },
        edit(){
            var self = this
            if(this.url){
                Promise.resolve().then(()=>{
                   return this.read_image(this.url)

                }).then((file)=>{
                        return cfg.pop_vue_com('com-image-crop',{file:file},{
                            title:false,
                            area: ['90%', '90%'],
                            shade: 0.8,
                            skin: 'img-shower',
                            shadeClose: true,
                        })
                } ).then((file1)=>{
                    if(! self.validate(file1)){
                        return Promise.reject()
                    }
                    if(self.cfg.maxspan){
                        return compressImage(file1,self.cfg.maxspan,0)
                    }else{
                        return file1
                    }
                }).then((file1)=>{
                    var files = [file1]
                    ex.uploads(files,this.up_url).then((url_list)=>{
                        self.url=url_list[0]
                        self.$emit('input',self.url)
                        self.$emit('select')
                    })
                })

            }

        },
        clear:function () {
            console.log('clear image data')
            this.img_files=''
            //this.url=''
            this.$emit('input','')
            this.$refs.file_input.clear()
        },
        rotate(){

            var crt= ex.parseSearch(this.url).rotate || 0
            this.url = ex.appendSearch(this.url,{rotate: (crt + 90) % 360})
        },
        validate:function(img_fl){
            //重载该函数，验证文件

            if(this.cfg.maxsize){
                if(img_fl.size > this.cfg.maxsize){
                    if(this.cfg.maxsize > 1024*1024){
                        var num_msg = (this.cfg.maxsize /(1024*1024) ).toFixed(2) + 'M'
                    }else  if(this.cfg.maxsize > 1024){
                        var num_msg = (this.cfg.maxsize /(1024) ).toFixed(2) + 'k'
                    }else{
                        var num_msg = this.cfg.maxsize
                    }
                    var msg = ex.template(cfg.tr.picture_size_excceed,{maxsize:num_msg})
                    cfg.showMsg(msg)
                    this.clear()
                    return false
                }
            }
            //console.log(img_fl.size)
            return true
        },
        select:function(){
            console.log('before select')
            var self=this
            if(! this.disable){
                $(this.$el).find('input[type=file]').click()
                this.disable=true
                setTimeout(function(){
                    self.disable=false
                },3000)

            }

            console.log('after select')
        }
    }
}

Vue.component('img-uploador',img_uploader)


/*
具备裁剪功能
==============
 img_crop是一种input

    <img-crop v-model='xxx' :config='{aspectRatio: 8 / 10}'></img-crop>
*
*  上传:
*  ======
*  fl.upload(xxx[0],function(urls){
*         ...
*  ))
* */

var img_crop={
    template: `<div class="img-crop">
    <!--<input type='file' @change='on_change($event)'-->
            <!--accept='image/*'>-->
    <!--<modal v-show='cropping' >-->
        <div class="total-wrap flex-v" style="width:80vw;height: 80vh;background-color: #ececec;">
            <div class="crop-wrap flex-grow">
                <img class="crop-img" :src="org_img" >
            </div>
            <div style="padding: 5px;">
            <div class="btn-group" role="group">
                <button class="btn btn-primary" @click="rotato_90()"><i class="fa fa-repeat" aria-hidden="true"></i></button>
                <button class="btn btn-primary" @click="zoom_in()"><i class="fa fa-search-plus" aria-hidden="true"></i></button>
                <button class="btn btn-primary" @click="zoom_out()"><i class="fa fa-search-minus" aria-hidden="true"></i></button>
            </div>
            <div class="btn-group" role="group">
                <button class="btn btn-primary" @click="make_sure()"><i class="fa fa-check" aria-hidden="true"></i></button>
                <button class="btn btn-primary" @click="cancel()"><i class="fa fa-times" aria-hidden="true"></i></button>
            </div>
            </div>
        </div>
    <!--</modal>-->
    </div>`,
    props:['ctx'],
    //props: ['value','config'],
    data: function () {
        var inn_config={
            size:{}
        }
        ex.assign(inn_config,this.ctx.config)

        return {
            files: [],
            org_img:'',
            cropping:false,
            inn_config:inn_config
        }
    },
    watch: {
        value: function (v) {
            // when input clear selected file, Component file-input need clear too.
            // Brower prohebit to set to Un-none string
            if (v == '') {
                this.$el.value = v
            }

        }
        ,
    },
    mounted(){
        this.set_value(this.ctx.file)
    },
    methods: {
        set_value(img_file){
            var self=this
            this.cropping=true
            //var img_file = event.target.files[0]
            fl.read(img_file,function (data) {
                self.org_img = data
                Vue.nextTick(function(){
                    self.init_crop()
                })
            })
        },
        cancel:function(){
            $(this.$el).find('input[type=file]').val('')
            this.cropping=false
        },
        zoom_in:function(){
            $(this.$el).find('.crop-img').cropper('zoom', 0.1);
        },
        zoom_out:function(){
            $(this.$el).find('.crop-img').cropper('zoom', -0.1);
        },
        rotato_90:function(){
            $(this.$el).find('.crop-img').cropper('rotate', 90);
        },
        move_img:function(){
            $(this.$el).find('.crop-img').cropper('setDragMode','move')
        },
        move_crop:function(){
            $(this.$el).find('.crop-img').cropper('setDragMode','crop')
        },
        //on_change: function (event) {
        //
        //    if($(this.$el).find('input[type=file]').val()==''){
        //        return
        //    }
        //    var self=this
        //    this.cropping=true
        //    var img_file = event.target.files[0]
        //
        //    //fl.read(img_file)
        //    //this.$emit('input', this.files)
        //    fl.read(img_file,function (data) {
        //        self.org_img = data
        //        Vue.nextTick(function(){
        //            self.init_crop()
        //        })
        //    })
        //},
        init_crop:function(){
            //$(this.$el).find('.crop-img').cropper({
            //    aspectRatio: 8 / 10,
            //});
            if(this.inn_config.aspectRatio){
                $(this.$el).find('.crop-img').cropper({aspectRatio:this.inn_config.aspectRatio});
            }

            $(this.$el).find('.crop-img').cropper('replace',this.org_img)
            $(this.$el).find('.crop-img').cropper('setDragMode','move')
        },
        make_sure:function(){
            var self=this
            // Upload cropped image to server if the browser supports `HTMLCanvasElement.toBlob`

            //$(this.$el).find('.crop-img').cropper('getCroppedCanvas',this.inn_config.size).toBlob(function (blob) {
            //    //var formData = new FormData();
            //    self.$emit('input',[blob])
            //    self.cropping=false
            //
            //});
            var data_url = $(this.$el).find('.crop-img').cropper('getCroppedCanvas',this.inn_config.size).toDataURL('image/jpeg')
            var blob=dataURLtoBlob(data_url)
            //self.$emit('input',[blob])
            self.cropping=false
            self.$emit('finish',blob)
        }
    }

}

function dataURLtoBlob(dataurl) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {type:mime});
}

Vue.component('com-image-crop',function(resolve,reject){
    ex.load_css(js_config.js_lib.cropper_css)
    ex.load_js(js_config.js_lib.cropper).then(()=>{
        resolve(img_crop)
    })
})





/*
* 下面是为了老代码的兼容性，以后不会用了。
*
*/

Vue.component('file-obj',{
    template:"<input model='filebody' type='file' @change='changed'>",
    props:{
        up_url:{
            type: String,
            required: true
        },
        //url:{
        //    type: String,
        //    twoWay:true
        //},
        ready:{}
    },
    methods:{
        changed:function (changeEvent) {
            var file=changeEvent.target.files[0];
            if(!file)
                return
            this.fd = new FormData();
            this.fd.append('file', file);
            this.ready=true;
            this.upload()
        },
        upload:function () {
            var self =this;
            $.ajax({
                url:this.up_url,
                type:'post',
                data:this.fd,
                contentType: false,
                cache: false,
                success:function (data) {
                    if(data.url){
                        self.$dispatch('rt_url',data.url)
                    }

                    //alert(data);
                    //self.url=data.url;
                    //self.$emit('url.changed',data.url)
                },
                //error:function (data) {
                //	alert(data.responseText)
                //},
                processData:false
            })
        }
    }
})


    Vue.component('logo-input',{
        props:['up_url','web_url','id'],
        template:`
          <div class='up_wrap logo-input'>
            <file-obj :id='id'
                accept='image/gif,image/jpeg,image/png'
                :up_url='up_url'
                @rt_url= 'get_web_url'>
            </file-obj>
            <div style="padding: 40px">
                <a class='choose'>Choose</a>
            </div>
            <div v-if='web_url' class="closeDiv">
            <div class="close" @click='clear()'>X</div>
            <img :src="web_url" alt="" class="logoImg">
            </div>
            </div>
        `,
        methods:{
            get_web_url:function(e){
                this.web_url=e
            },
            clear:function () {
                this.web_url=''
                $('#'+this.id).val('')
            }
        }
    })



window.fl=fl


////压缩图片
function compressImage  (file,maxspan,Orientation)  {
    // 图片小于1M不压缩
    //if ( file.size < Math.pow(1024, 2)) {
    //    return success(file);
    //}

    return new Promise(function(resolve,reject){
        const name = file.name; //文件名
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (e) => {
            const src = e.target.result;
            const img = new Image();
            img.src = src;
            img.onload = (e) => {
                const w = img.width;
                const h = img.height;
                var span =  Math.max(w,h)
                if(maxspan > span){
                    console.log('small than '+maxspan)
                    resolve(file)
                    return
                }
                var ratio = maxspan / span
                var real_w = w * ratio
                var real_h = h * ratio
                const quality = 0.92;  // 默认图片质量为0.92
                //生成canvas
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                // 创建属性节点
                const anw = document.createAttribute("width");
                anw.nodeValue = real_w   // w;
                const anh = document.createAttribute("height");
                anh.nodeValue = real_h //h;
                canvas.setAttributeNode(anw);
                canvas.setAttributeNode(anh);

                // 旋转图像方向
                var width = real_w
                var height = real_h
                var drawWidth = width
                var drawHeight = height
                var degree =0
                switch(Orientation){
                    //iphone横屏拍摄，此时home键在左侧
                    case 3:
                        degree=180;
                        drawWidth=-width;
                        drawHeight=-height;
                        break;
                    //iphone竖屏拍摄，此时home键在下方(正常拿手机的方向)
                    case 6:
                        canvas.width=height;
                        canvas.height=width;
                        degree=90;
                        drawWidth=width;
                        drawHeight=-height;
                        break;
                    //iphone竖屏拍摄，此时home键在上方
                    case 8:
                        canvas.width=height;
                        canvas.height=width;
                        degree=270;
                        drawWidth=-width;
                        drawHeight=height;
                        break;
                }
                //使用canvas旋转校正
                ctx.rotate(degree*Math.PI/180);

                //铺底色 PNG转JPEG时透明区域会变黑色
                ctx.fillStyle = "#fff";
                ctx.fillRect(0, 0, drawWidth, drawHeight);

                //ctx.drawImage(img, 0, 0, w, h);
                ctx.drawImage(img, 0, 0, drawWidth, drawHeight);
                // quality值越小，所绘制出的图像越模糊
                const base64 = canvas.toDataURL('image/jpeg', quality); //图片格式jpeg或webp可以选0-1质量区间

                // 返回base64转blob的值
                console.log(`原图${(src.length/1024).toFixed(2)}kb`+ `新图${(base64.length/1024).toFixed(2)}kb`);
                if(src.length < base64.length){
                    resolve(file)
                    return
                }
                //去掉url的头，并转换为byte
                const bytes = window.atob(base64.split(',')[1]);
                //处理异常,将ascii码小于0的转换为大于0
                const ab = new ArrayBuffer(bytes.length);
                const ia = new Uint8Array(ab);
                for (let i = 0; i < bytes.length; i++) {
                    ia[i] = bytes.charCodeAt(i);
                }
                file = new Blob( [ab] , {type : 'image/jpeg'});
                file.name = name;

                resolve(file);
            }
            img.onerror = (e) => {
                reject(e);
            }
        }
        reader.onerror = (e) => {
            reject(e);
        }
    })

}