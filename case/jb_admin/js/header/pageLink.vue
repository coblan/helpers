<template>
  <div class="com-head-page-link" :class="{active:is_active}" @click="on_click()" :style="mystyle">
    <span v-text="ctx.label"></span>
  </div>
</template>

<script>
export default {
  props:['ctx'],
  name: "pageLink.vue",
  computed:{
    mystyle(){
      return {
        '--width':this.ctx.width || 'auto'
      }
    },
    is_active(){
      return ex.eval(this.ctx.active_express)
    }
  },
  methods:{
    on_click(){
        ex.eval(this.ctx.click_express,{})
    }
  }
}
</script>

<style scoped lang="scss">
.com-head-page-link{
  height: 100%;
  //display: flex;
  //align-items: center;
  display: inline-block;
  width: var(--width);
  padding: 15px 0;
  text-align: center;
  color: white;
  cursor: pointer;
  &.active{
    background-color: rgba(255,255,255,.6);
    color: white; text-shadow: black 0.1em 0.1em 0.2em
    //color: #696868;
  }

}

</style>