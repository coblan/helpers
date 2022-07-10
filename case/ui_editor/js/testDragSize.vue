<template>
  <div class="box">
    <div class="left">
      <slot name="left"></slot>
    </div>
    <div class="resize"></div>
    <div class="right">
      <slot name="right"></slot>
    </div>
  </div>
</template>
<script>
import ex from 'weblib/ex'
export default {
  props:{
    saveName:{},
  },
  mounted(){
    var self = this
      var resize = this.$el.querySelector(".resize");
      var left = this.$el.querySelector(".left");
      var right = this.$el.querySelector(".right");
      var box = this.$el;
      resize.onmousedown = function(e){
        var startX = e.clientX;
        resize.left = resize.offsetLeft;
        document.onmousemove = function(e){
          var endX = e.clientX;

          var moveLen = resize.left + (endX - startX);
          var maxT = box.clientWidth - resize.offsetWidth;
          if(moveLen<10) moveLen = 10;
          if(moveLen>maxT-10) moveLen = maxT-10;

          resize.style.left = moveLen;
          left.style.width = moveLen + "px";
          right.style.width = (box.clientWidth - moveLen - 5) + "px";

        }
        document.onmouseup = function(evt){
          document.onmousemove = null;
          document.onmouseup = null;
          resize.releaseCapture && resize.releaseCapture();
          if(self.saveName){
            ex.localSet(self.saveName,{left: left.style.width,right:right.style.width})
          }
        }
        resize.setCapture && resize.setCapture();
        return false;
      }
      if(this.saveName){
          var size= ex.localGet(this.saveName,{})
          left.style.width = size.left;
          right.style.width = size.right;
      }
  },
  methods:{
    restoreSize(){

    }
  }
}
</script>
<style scoped lang="scss">

//.box{
//  width:600px;
//  height:500px;
//  overflow:hidden;
//}
.box{
  display: flex;

}
.left{

  height:100%;
  //background:skyblue;
  //float:left;
}

.resize{
  width:5px;
  height:100%;
  cursor: w-resize;
  background-color: #f4f4f4;
  //float:left;
}

.right{
  //float:right;
  //width:70%;
  height:100%;
  //background:tomato;
}
</style>