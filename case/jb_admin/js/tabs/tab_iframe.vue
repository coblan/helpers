<template>
<iframe :src="src" class="com-tab-iframe">
  sssg
</iframe>
</template>

<script>
export default {
  name: "tab_iframe.vue",
  props:['tab_head','par_row'],
  data(){
    return {
      src:''
    }
  },
  mounted(){
    if(this.tab_head.mounted_express){
      ex.eval(this.tab_head.mounted_express,{vc:this,par_row:this.par_row,head:this.tab_head})
    }
  }
}
</script>

<style scoped lang="scss">
.com-tab-iframe{
  width: 100%;
  height: 100%;
  border: none;
}
</style>