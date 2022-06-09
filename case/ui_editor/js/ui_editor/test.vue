<template>
  <div>
      test {{text}}
  </div>
</template>
<script>
export default {
  props:{
    text:{}
  },
  methods:{
  },

}
cfg.ui_editor['uie-test'] = {
    fields:[
      {name:'text',label:'label',editor:'com-field-linetext'}
    ],
    desp:'测试组件'
}
</script>
