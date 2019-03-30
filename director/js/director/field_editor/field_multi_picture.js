require('./scss/field_multi_picture.scss')

Vue.component('com-field-multi-picture',{
    props:['row','head'],
    template:`<div class="com-field-multi-picture">
    <textarea style="display: none;" :name="head.name" id="" cols="30" rows="10" v-model="row[head.name]"></textarea>

        <div style="vertical-align: top" >
            <div v-if="!head.readonly" class="add-btn" @click="open_select_images()" style="width: 100px;height: 100px;position: relative;display: inline-block;padding: 10px">
                <div class="inn-btn"  style="">
                    <span class="center-vh" style="font-size: 300%;">+</span>
                </div>
            </div>
            <div class="img-wrap" v-for="(imgsrc,index) in row[head.name]" @click="big_win(imgsrc)">
                <img class="center-vh" :src="imgsrc" alt="图片不能加载">
                <div v-if="!head.readonly" class="close" @click='remove_image(index)'><i class="fa fa-times-circle" aria-hidden="true" style="color:red;position:relative;left:30px;"></i></div>
            </div>
        </div>
         <file-input v-if="!head.readonly" style="display: none"  v-model='img_files'
            accept='image/*'  multiple></file-input>
       	</div>`,
    data:function(){
        return {
            img_files:[],
        }
    },
    watch:{
        img_files:function(v,old){
            if(!v){
                return
            }
            var self=this
            console.log('start upload')
            if(v==""){
                return
            }
            if(! self.validate(v)){
                return
            }
            var up_url = this.head.up_url || '/d/upload?path=general_upload/images'
            fl.uploads(v,up_url,function(url_list){
                if(!self.row[self.head.name]){
                    self.row[self.head.name] = url_list
                }else{
                    self.row[self.head.name] = self.row[self.head.name].concat(url_list)
                }
                self.img_files = []
                //self.$emit('input',self.img_files)
                self.$emit('select')
            })
        }
    },
    methods:{
        big_win:function(imgsrc){
            var ctx = {imgsrc:imgsrc}
            pop_layer(ctx,'com-pop-image',function(){},{
                title:false,
                area: ['90%', '90%'],
                shade: 0.8,
                skin: 'img-shower',
                shadeClose: true,
            })
        },
        remove_image:function(index){
            var image_list = this.row[this.head.name]
            image_list.splice(index,1)
        },
        validate:function(image_files){
            //重载该函数，验证文件

            //if(this.cfg.maxsize){
            //    if(img_fl.size > this.cfg.maxsize){
            //        var msg = ex.template(cfg.tr.picture_size_excceed,{maxsize:this.cfg.maxsize})
            //        cfg.showMsg(msg)
            //        this.clear()
            //        return false
            //    }
            //}
            return true
        },
        open_select_images:function(){
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
        on_uploader_click:function(){
            $(this.$el).find('.virtual_input').focus()
        }
    }
})


Vue.component('com-pop-image',{
    props:['ctx'],
    data:function(){
        return {
            crt_view:'2d',
            read_3d:''
        }
    },
    computed:{
        wraped_3d:function(){
            return '/3d_wrap?d3_url='+encodeURIComponent(this.ctx.floor.img_3d)
        }
    },
    methods:{
        start_read:function(){
            this.read_3d= this.wraped_3d
        }
    },
    template:`<div class="com-pop-image"  style="position: absolute;top:0;left: 0;bottom: 0;right: 0;">
             <img  class="center-vh" :src="ctx.imgsrc" style="max-width: 95%;max-height:95%" alt="">
    </div>`
})
