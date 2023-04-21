<template>
  <div class="com-widget-stack">
<!--      <TransitionGroup  name="slide_leftToRight">-->
        <component v-for="(ctx,index) in ctx_list" v-show="index==ctx_list.length-1" :class="`myitem_${index}`"
                   :is="ctx.widget" :ctx="ctx" v-bind="ctx" @win-event="$emit('win-event',$event)"></component>
<!--      </TransitionGroup>-->
  </div>
</template>
<script>
import animate from 'weblib/ex/animate.js'

export default {
  props:['ctx_list'],
  data(){
      return {
        last_length:this.ctx_list.length
      }
  },
  computed:{
    list_length(){
      return this.ctx_list.length
    }
  },
  mounted(){
    Vue.nextTick(()=>{
      var dom = this.$el.querySelector(`.myitem_0`)
      animate.animateCss (dom,'fadeIn')
    })
  },
  watch:{
    list_length(nv,ov){
      Vue.nextTick(()=>{
        var dom = this.$el.querySelector(`.myitem_${nv-1}`)
        if(nv>ov){
          animate.animateCss (dom,'fadeIn')
          console.log('进入')
        }else{
          animate.animateCss (dom,'fadeIn')
          console.log('退出')
        }
      })

    }
  }
}
</script>
<style scoped lang="scss">
.com-widget-stack{
  position: absolute;
  bottom: 0;
  top: 0;
  left: 0;
  right: 0;
}
//.v-enter, .v-leave-to {
//  transform: translateX(100%);
//}
/*滑动(滑入)——从左侧滑入,从右侧滑出*/
.slide_leftToRight-enter-active {
  animation: slideIn_left 1s;
}

/*滑动(滑出)——从左侧滑入,从右侧滑出*/
.slide_leftToRight-leave-active {
  animation: slideOut_right 1s;
}

/*滑入——从左侧*/
@keyframes slideIn_left {
  0% {
    left: -100%;
  }
  100% {
    left: 0;
  }
}
/*滑出——从右侧*/
//@keyframes slideOut_right {
//  0% {
//    left: 0;
//  }
//  100% {
//    left: 100%
//  }
//}
</style>