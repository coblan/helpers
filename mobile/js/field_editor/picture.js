require('./styl/picture.styl')

Vue.component('com-field-picture',{
    props:['row','head'],
    template:` <van-cell class="com-field-picture" :title="head.label" >
        <template v-if="!head.readonly">
             <textarea style="display: none;" :name="head.name" id="" cols="30" rows="10" v-model="row[head.name]"></textarea>
            <div class="picture-panel" style="vertical-align: top" >
              <div v-if="!row[head.name]" class="center-vh choose-btn" @click="open_select_images()">Choose</div>

               <div class="picture-content" v-else
               :style="{backgroundImage:'url('+ row[head.name]  +')'}"
               @click="big_win(row[head.name])">
                    <!--<img :src="row[head.name]" alt="">-->
                    <div v-if="!head.readonly" class="close" @click.stop='remove_image()'><i class="fa fa-times-circle" aria-hidden="true" style="color:red;position:relative;left:30px;"></i></div>
               </div>

            </div>
            <input class="my-file-input"  style="display: none"
                type='file' accept='image/*'  @change='on_change($event)'>

        </template>
           <div class="picture-content" v-else
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
            let new_selected_files = event.target.files
            this.uploadImage( new_selected_files )
            $(this.$el).find('.my-file-input').val('')
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
})