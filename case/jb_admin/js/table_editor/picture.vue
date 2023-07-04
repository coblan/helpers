<template>
  <span>
<!--     <img @load='loaded=true' :style="cusStyle"  @click="open()" :src="src" alt="" height="96px" style="cursor: pointer;">-->
    <aesImage @load='loaded=true' :style="cusStyle"  @click.native="open()" :src="src" alt="" height="96px"
              @real_src="onRealSrc"
              style="cursor: pointer;">
    </aesImage>

  </span>
</template>
<script>
import aesImage from 'webcase/h5uis/aesImage.vue'
export default {
  components:{
    aesImage
  },
  props:['rowData','field','index'],
  data:function(){
    return {
      loaded:false,
      real_src:''
    }
  },
  watch:{
    src:function(){
      this.loaded=false
    }
  },
  computed:{
    src:function(){
      return this.rowData[this.field]
    },
    cusStyle:function(){
      if(!this.loaded){
        return {
          visibility:'hidden'
        }
      }else{
        return {
          visibility:'visible'
        }
      }
    }
  },
  methods:{
    onRealSrc(e){
      this.real_src = e
    },
    open:function(){
//window.open(this.rowData[this.field])
      var ctx = {imgsrc:this.real_src}
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




