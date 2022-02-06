<template>

  <div class="head-item page-label">
{{my_label}}
  </div>


</template>
<script>
export default {
  props:['ctx'],
  data(){
    return {
      my_label:''
    }
  },
  mounted(){
    live_root.$on('tab-change',this.setLabel)
    // this.$nextTick(()=>{
    //   live_root.$on('tab-change',this.setLabel)
    // })

  },
  watch:{

  },
  methods:{
    setLabel(tab_ctx){
      this.my_label = tab_ctx.label
    }
  }
}
</script>
<style scoped lang="scss">
.head-item{
  display:  inline-block;
  padding: 15px 0;
  //background-color: #252f34;
  //background-color: white;
}
.page-label{
  margin-left: 10px;
}
</style>