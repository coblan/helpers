
<template>
  <div class="com-field-picture picture">
    <template v-if="head.readonly">
      <aesImage  class="img-uploador clickable" v-if='row[head.name]' @click.native="on_click_image(real_image_src)"
                 :src='abs_url ' :image-src.sync="real_image_src"> </aesImage>
      <span v-else>---</span>
    </template>
    <template  v-else>
      <input class="virtual_input"
             style="position:absolute;height: 0;width: 0;" type="text"  :name="head.name" v-model="row[head.name]">
      <img-uploador @select="on_uploader_click()" :up_url="uploadUrl" v-model="row[head.name]" :id="'id_'+head.name" :config="head">
        <template v-slot:show>
          <aesImage  class="img-uploador clickable  logoImg"
                     v-if='row[head.name]' @click.native="on_click_image(real_image_src)"
                     :src='abs_url' :image-src.sync="real_image_src"> </aesImage>
        </template>
      </img-uploador>
    </template>
  </div>
</template>
<script>
import aesImage from 'webcase/h5uis/aesImage.vue'
export default {
  components:{
    aesImage,
  },
  props:['row','head'],
  data(){
    return {
        real_image_src:'',
        abs_url:'',
    }
  },
  mounted(){
    if(this.head.mounted_express){
      ex.eval(this.head.mounted_express,{vc:this,head:this.head})
    }
    this.absImageUrl()
  },
    watch:{
      outvalue(nv){
           alert('bb')
          this.absImageUrl()
      }
    },
    computed:{
      outvalue(){
        return this.row[this.head.name]
      },
      uploadUrl(){
        if(this.head.upload_url_express){
          var rr = ex.eval(this.head.upload_url_express,{vc:this})
          return rr
        }else{
          var rt =  this.head.upload_url || this.head.up_url
          var search = ex.parseSearch(rt)
          if (this.head.aes && !search.aes){
            rt = ex.appendSearch(rt,{aes:'ecb'})
          }
          if(this.head.maxspan && !search.quality){
            rt = ex.appendSearch(rt,{quality:'70'})
          }
          return  rt
        }
      }
    },
  methods:{
    async absImageUrl(){
      var imageurl = this.row[this.head.name]
      if(!imageurl){
        this.abs_url = imageurl
        return
      }

      if(imageurl.startsWith('http')){
        this.abs_url = imageurl
      }else if(this.head.cdn){
        this.abs_url =  `${this.head.cdn}${imageurl}`
      }else if(this.head.abs_url_express){
        var resp = await ex.eval(this.head.abs_url_express,{vc:this,head:this.head,imageUrl:imageurl})
        if(resp){
          this.abs_url = resp
        }
      }else{
        this.abs_url = imageurl
      }
    },
    on_uploader_click:function(){
      $(this.$el).find('.virtual_input').focus()
    },
    on_click_image(url){
      var ctx = {imgsrc:url }
      pop_layer(ctx,'com-pop-image',function(){},{
        title:false,
        area: ['90%', '90%'],
        shade: 0.8,
        skin: 'img-shower',
        shadeClose: true,
      })
    }
  }
}
</script>
