<template>
  <div class="com-pop-image"  style="position: absolute;top:0;left: 0;bottom: 0;right: 0;">
    <img  @wheel.prevent = "onwheel" class="center-vh" :src="ctx.imgsrc" :style="mystyle" alt="">
  </div>
</template>
<script>
export default {
  props:['ctx'],
  data:function(){
    return {
      crt_view:'2d',
      read_3d:'',
      scale:1,
      maxwidth:0,
    }
  },
  computed:{
    wraped_3d:function(){
      return '/3d_wrap?d3_url='+encodeURIComponent(this.ctx.floor.img_3d)
    },
    mystyle(){

      return {
        'max-width': 95*this.scale + '%',
        'max-height':95*this.scale + '%',
      }
    }
  },
  methods:{
    start_read:function(){
      this.read_3d= this.wraped_3d
    },
    onwheel(e){

      if (e.deltaY > 0){
        var width = $(this.$el).find('img').width()
        console.log(width)
        if (width >this.maxwidth){
          this.maxwidth = width
          this.scale += 0.1
        }
      }
      if (e.deltaY < 0){
        this.maxwidth =0
        this.scale -= 0.1
      }
    }
  },

}
</script>
