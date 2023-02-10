<template>
  <div style="display: flex;align-items: center">
<!--    <component style="display: inline-block" :is="com.editor" v-for="com in head.components" :row="row" :head="com"></component>-->
    <div class="mt"></div>
  </div>
</template>
<script>
export  default  {
  props:['row','head'],
  mounted(){
    var self =this
    var mydict = {}
    ex.each(self.head.components,com=>{
      mydict[com.name] = `<component style="display: inline-block" is="${com.editor}" :row="row" :head="head_dict.${com.name}"></component> `
    })
    var MyComponent = Vue.extend({
      template: ex.template(this.head.template,mydict) ,
      data(){
        var head_dict = {}
        ex.each(self.head.components,com=>{
          head_dict[com.name] = com
        })
        return {
          row:self.row,
          head:self.head,
          head_dict:head_dict,
        }
      },

    })
    new MyComponent().$mount(this.$el.querySelector('.mt'))
  }
}
</script>