<template>
  <div class="uie-mount-view">

    <template v-for="head in normed_heads">
      <component v-if="head.children" :is="head.editor" :key="head.id"  v-bind="head.bind" :children="head.children" :id="head.id"></component>
      <component v-else :is="head.editor" :key="head.id"  v-bind="head.bind" :id="head.id"></component>
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
          if(resp){
            ex.vueAssign(head.bind,resp)
          }

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

cfg.ui_editor['uie-mount-view'] = {
  has_bind_express:true,
  fields:[
    {name:'pageName',label:'页面名',editor:'com-field-linetext'},
  ],
  desp:'mountview',
  help_text:`
<div>数据结构</div>

  `
}
</script>