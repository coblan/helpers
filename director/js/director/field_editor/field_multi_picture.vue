<template>
  <div class="com-field-multi-picture">
    <textarea style="display: none;" :name="head.name" id="" cols="30" rows="10" v-model="row[head.name]"></textarea>

    <div style="vertical-align: top" >
      <div v-if="!head.readonly" class="add-btn" @click="open_select_images()"
           style="width: 100px;height: 100px;position: relative;display: inline-block;padding: 10px">
        <div class="inn-btn"  style="">
          <span class="center-vh" style="font-size: 300%;">+</span>
        </div>
      </div>

        <div class="img-wrap" v-for="(imgsrc,index)  in row[head.name]"  :key="imgsrc">
<!--              <img class="center-vh" :src="imgsrc" alt="图片不能加载" @click="big_win(imgsrc)">-->
          <aseImage class="center-vh" :src="absImageUrl( imgsrc) "
                    @imageSrc="image_url_dc[imgsrc] = $event"
                    @click.native="big_win(image_url_dc[imgsrc])" ></aseImage>
          <div v-if="!head.readonly" class="close" @click='remove_image(index)'>
            <i class="fa fa-times-circle" aria-hidden="true" style="color:red;position:relative;left:30px;"></i>
          </div>
        </div>


    </div>

    <file-input v-if="!head.readonly" style="display: none"  v-model='img_files'
                accept='image/*'  multiple></file-input>
  </div>
</template>
<script>
import  popImage from './popImage.vue'
import  aseImage from 'webcase/h5uis/aesImage.vue'
export default  {
  components:{
    popImage,
    aseImage
  },
  props:['row','head'],
  data:function(){
    return {
      img_files:[],
      image_urls:this.row[this.head.name],
      image_url_dc:{},
    }
  },
  mounted(){
      if(this.row[this.head.name]==undefined){
        Vue.set(this.row,this.head.name,[])
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
      if(this.head.up_url){
        var up_url= this.head.up_url
      }else{
        var up_url =  '/d/upload?path=general_upload/images'
        if(this.head.aes){
          up_url = ex.appendSearch(up_url,{aes:this.head.aes})
        }
        if(this.head.maxspan){
          up_url = ex.appendSearch(up_url,{quality:70})
        }
      }

      cfg.show_load('uploading...')
      fl.uploads(v,up_url,function(url_list){
        cfg.hide_load()
        if(!self.row[self.head.name]){
          self.row[self.head.name] = url_list
        }else{
          self.row[self.head.name] = self.row[self.head.name].concat(url_list)
        }
        self.img_files = []
        //self.$emit('input',self.img_files)
        self.$emit('select')
      })
    },
  },
  methods:{
    absImageUrl(imageurl){
      if(imageurl.startsWith('http')){
        return imageurl
      }else if(this.head.cdn){
          return  `${this.head.cdn}${imageurl}`
      }else{
        return  imageurl
      }
    },
    big_win:function(imgsrc){
      var ctx = {imgsrc:imgsrc}
      pop_layer(ctx,popImage,function(){},{
        title:false,
        area: ['90%', '90%'],
        shade: 0.8,
        skin: 'img-shower',
        shadeClose: true,
      })
    },
    remove_image:function(index){
      debugger
     var image_list = this.row[this.head.name]
      image_list.splice(index,1)
      Vue.set(this.row,this.head.name,image_list)
      // this.row[this.head.name].splice(index,1)

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
}
</script>
<style scoped lang="scss">
.com-field-multi-picture{
.picture-panel{
  display: flex;
  align-items: center;
}
.img-wrap{
  display: inline-block;
  position: relative;
  width: 100px;
  height: 100px;
  vertical-align: top;
  margin:10px;
}
.img-wrap  img{
  max-width:100%;
  max-height:100%;
}
.add-btn{
  margin:10px;
.inn-btn{
//background-color: #e2e2e2;
  background-color: #FBFDFF;
  border: 1px solid #a7bad2;
  border-radius: 6px;
  width: 40px;
  height: 40px;
  position: relative;
  color: #8C939D;
  transition: all .5s;
}
.inn-btn:hover{
//background-color: #efefef;
  border: 1px solid #66B1FF;;
  background-color: rgba(102,177,255,0.3);
  cursor: pointer;
}
}
}

.layui-layer.img-shower{
  background-color: rgba(0,0,0,0.3) ;
}
</style>