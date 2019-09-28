require('./styl/picture.styl')

export var com_picture = {
    props:['row','head'],
    template:` <van-cell class="com-field-picture" :class="{'van-cell--required':head.required && !head.readonly,}" :title="head.label" >
        <template v-if="!head.readonly">
             <textarea style="display: none;" :name="head.name" id="" cols="30" rows="10" v-model="row[head.name]"></textarea>
            <div class="picture-panel" style="vertical-align: top" >
              <div v-if="!row[head.name]" class="center-vh choose-btn" @click="open_select_images()" v-text="head.placeholder || 'Choose'"></div>

               <div class="picture-content" v-else
               :style="{backgroundImage:'url('+ row[head.name]  +')'}"
               @click="big_win(row[head.name])">
                    <div v-if="!head.readonly" class="close" @click.stop='remove_image()'><i class="fa fa-times-circle" aria-hidden="true" style="color:red;position:relative;left:30px;"></i></div>
               </div>

            </div>
            <input class="my-file-input"  style="display: none"
                type='file' accept='image/*'  @change='on_change($event)'>

        </template>
           <div class="picture-content" v-else-if="row[head.name]"
               :style="{backgroundImage:'url('+ row[head.name]  +')'}"
               @click="big_win(row[head.name])">
           </div>

    </van-cell>`,
    data(){
        return {
        }
    },
    methods:{
        on_change(event){
            //let new_selected_files = event.target.files
            var self =this
            var ls = ex.map(event.target.files,(file) => {
                return new Promise(function(resolve_outer,reject_outer){
                    new Promise(function(resolve,reject){
                        EXIF.getData(file, function() {
                            var Orientation = EXIF.getTag(this, 'Orientation')
                            resolve(Orientation)
                        })
                    }).then((Orientation)=>{
                        if( self.head.maxspan ){
                            return compressImage(file,self.head ,Orientation)
                        }else{
                            return file
                        }
                    }).then(rt=>{
                        resolve_outer(rt)
                    })
                })
            })
            Promise.all(ls) .then((results)=>{
                var new_selected_files= results
                this.uploadImage( new_selected_files )
                $(this.$el).find('.my-file-input').val('')
            })

        },
        uploadImage(image_files){
            if(!image_files){
                return
            }
            var self=this
            console.log('start upload')

            var up_url = this.head.up_url || '/d/upload?path=general_upload/images'
            cfg.show_load()
            ex.uploads(image_files,up_url,function(url_list){
                cfg.hide_load()
                Vue.set(self.row,self.head.name,url_list[0])
            })
        },
        open_select_images(){
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
        },
        remove_image(){
            this.row[this.head.name]=""
            //var image_list = this.row[this.head.name]
            //image_list.splice(index,1)
        },
        big_win(imgsrc){
            //var image_list = this.row[this.head.name]
            //var index = image_list.indexOf(imgsrc)
            vant.ImagePreview({
                    images:[imgsrc],
                    startPosition: 0,
                }
            );
        },
    }
}


Vue.component('com-field-picture',function(resolve,reject){
    ex.load_js('https://cdn.jsdelivr.net/npm/exif-js').then(()=>{
        resolve(com_picture)
    })
})

//this.compressImage(files[0], (file)=>{
//    console.log(file);
//    const formData = new FormData();
//    formData.append('file', file, file.name || '上传图片.jpeg');
//}, $.noop);
////压缩图片
 function compressImage  (file,option,Orientation)  {
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
                if(option.maxspan > span){
                    alert(span )
                    resolve(file)
                    return
                }
                var ratio = option.maxspan / span
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