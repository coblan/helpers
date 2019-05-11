require('./styl/bool.styl')

Vue.component('com-field-bool',{
    props:['row','head'],
    template:` <van-cell class="com-field-bool" :title="head.label" >
        <van-checkbox v-model="row[head.name]">
        </van-checkbox>
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
            //if(! self.validate(v)){
            //    return
            //}
            var up_url = this.head.up_url || '/d/upload?path=general_upload/images'
            cfg.show_load()
            ex.uploads(image_files,up_url,function(url_list){
                cfg.hide_load()
                if(!self.row[self.head.name]){
                    Vue.set(self.row,self.head.name,url_list)
                    //self.row[self.head.name] = url_list
                }else{
                    self.row[self.head.name] = self.row[self.head.name].concat(url_list)
                }
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
        remove_image(index){
            var image_list = this.row[this.head.name]
            image_list.splice(index,1)
        },
        big_win(imgsrc){
            var ctx = {imgsrc:imgsrc}
            pop_layer(ctx,'com-pop-image',function(){},{
                title:false,
                area: ['90%', '90%'],
                shade: 0.8,
                skin: 'img-shower',
                shadeClose: true,
            })
        },
    }
})