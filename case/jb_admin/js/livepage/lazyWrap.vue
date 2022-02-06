<template>
  <div class="com-lazy-wrap"></div>
</template>

<script>
/*
* 用于封装延迟加载的tab页面
* */
export default {
  props:['ctx'],
  mounted(){
    if(this.ctx.lazy_director_name){
      this.getCtxFromDirectorName(this.ctx.lazy_director_name)
    }
    // if(this.ctx.lazy_init){
    //   ex.eval(this.ctx.lazy_init,{head:this.ctx})
    // }

  },
  methods:{
    async getCtxFromDirectorName(name){
      cfg.show_load();
      var resp = await  ex.director_call(name,{})
      cfg.hide_load()
      ex.vueAssign(this.ctx,resp)
    }
  }
}
</script>


