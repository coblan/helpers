<template>
  <div class="uie-mount-view">

    <template v-for="head in inn_heads">
      <component v-if="head.children" :is="head.editor" :key="head.id"  v-bind="head.bind" :children="head.children"></component>
      <component v-else :is="head.editor" :key="head.id"  v-bind="head.bind"></component>
    </template>

  </div>
</template>
<script>
import ex from 'weblib/ex'
export default {
  props:{
    heads:{},
    pageName:{},
  },
  data(){
    return {
        inn_heads:this.heads
    }
  },
  async mounted(){
    if(this.pageName){
      var resp = await ex.director_call('uie/page',{name:this.pageName} )
      this.inn_heads = resp
    }
  }
}
</script>