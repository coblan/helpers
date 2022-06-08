<template>
  <div class="uie-mount-view">

    <template v-for="head in normed_heads">
      <component v-if="head.children && head.loaded" :is="head.editor" :key="head.id"  v-bind="head.bind" :children="head.children"></component>
      <component v-else-if="head.loaded" :is="head.editor" :key="head.id"  v-bind="head.bind"></component>
    </template>

  </div>
</template>
<script>
import ex from 'weblib/ex'
export default {
  props:{
    heads:{
      default:()=>[]
    },
    pageName:{},
  },
  data(){
    if(this.heads){
      this.adaptHeads(this.heads)
    }
    return {
        inn_heads:this.heads
    }
  },

  async mounted(){
    if(this.pageName){
      var resp = await ex.director_call('uie/page',{name:this.pageName} )
      this.inn_heads = resp
      this.adaptHeads(this.inn_heads)
    }
  },
  computed:{
    normed_heads(){
        var myheads =[]
        function checkheads(heads){
          var local_heads = []
          ex.each(heads,head=>{
            if(head.loaded){
              var t_head = ex.copy(head)
              if(head.children){
                t_head.children = checkheads(head.children)
              }
              local_heads.push(t_head)
            }
          })
          return local_heads
        }
        myheads = checkheads(this.inn_heads)
      return myheads
    }
  },
  methods:{
    adaptHeads(heads){
      ex.each(heads, async (head)=>{
        if(head.bind_express){
          head.loaded = false
          var resp = await ex.eval(head.bind_express,{ex:ex,head:head})
          ex.vueAssign(head.bind,resp)
          head.loaded = true


        }else{
          head.loaded = true
        }
        if(head.children){
          this.adaptHeads(head.children)
        }
      })
    }
  }
}
</script>