<template>
  <div style="height: 96px">
<!--    设置96的高度，防止table组件计算高度出问题，造成不能滚动-->
<!--     <img @load='loaded=true' :style="cusStyle"  @click="open()" :src="src" alt="" height="96px" style="cursor: pointer;">-->
    <aesImage @load='loaded=true' :style="cusStyle"  @click.native="open()" :src="src" alt=""
              :image-src.sync='real_src'
              style="cursor: pointer;height: 96px">
    </aesImage>

  </div>
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




