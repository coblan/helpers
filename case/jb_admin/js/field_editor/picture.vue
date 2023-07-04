
<template>
  <div class="com-field-picture picture">
    <template v-if="head.readonly">
      <aesImage  class="img-uploador clickable" v-if='row[head.name]' @click.native="on_click_image(real_image_src)"
                 :src='row[head.name]' :image-src.sync="real_image_src"> </aesImage>
      <span v-else>---</span>
    </template>
    <template  v-else>
      <input class="virtual_input"
             style="position:absolute;height: 0;width: 0;" type="text"  :name="head.name" v-model="row[head.name]">
      <img-uploador @select="on_uploader_click()" :up_url="uploadUrl" v-model="row[head.name]" :id="'id_'+head.name" :config="head">
        <template v-slot:show>
          <aesImage  class="img-uploador clickable  logoImg"
                     v-if='row[head.name]' @click.native="on_click_image(real_image_src)"
                     :src='row[head.name]' :image-src.sync="real_image_src"> </aesImage>
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
        real_image_src:''
    }
  },
    computed:{
      uploadUrl(){
        debugger
        if(this.head.upload_url_express){
          var rr = ex.eval(this.head.upload_url_express,{vc:this})
          return rr
        }else{
          var rt =  this.head.upload_url || this.head.up_url
          debugger
          if (this.head.aes){
            rt = ex.appendSearch(rt,{aes:'ecb'})
          }
          return  rt
        }
      }
    },
  methods:{
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
