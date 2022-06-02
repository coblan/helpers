<template>
  <div>
    <component v-for="item in children" :is="item.editor" v-bind="item.bind"></component>
  </div>
</template>
<script>
export default {
  props:{
    children:[]
  }
}

cfg.ui_editor['uie-general-wrap'] = {
  has_children:true,
  fields:[
    {name:'director_name',label:'director name',editor:'com-field-linetext'},
  ]
}
</script>

