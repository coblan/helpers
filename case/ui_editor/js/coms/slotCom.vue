<template>
  <div>
    aa
  </div>
</template>
<script>
export default {
    data(){
      var childStore= new Vue()
      childStore.name='slot-com'
      return {
        childStore:childStore
      }
    }
}

cfg.ui_editor['uie-slot-com'] = {
  has_children:true,
  has_bind_express:true,
  fields:[
    {name:'name',label:'组件名',editor: 'com-field-linetext'},
  ],
  desp:'slot组件的根元素',
  help_text:`
  <div>容器,对应vue的slot功能</div>
  `
}
</script>