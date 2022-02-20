<template>
  <div class="menu-image-icon" :class="ctx.class">
    <img :src="ctx.image_url" alt="">
    <img class="my-active" :src="ctx.active_image_url" alt="">
  </div>
</template>
<script>

export  default  {
  props:{
    ctx:{
    }
  },
  mounted(){
    if(this.ctx.css){
      ex.append_css(this.ctx.css)
    }
  },
}
</script>
<style scoped lang="scss">
.menu-image-icon{
  display: inline-block;
  .my-active{
    display: none;
  }
}
.active{
  display: inline-block;
}
img{
  height: 1em;
  width: 1em;
}
</style>