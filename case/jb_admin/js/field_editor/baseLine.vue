<template>
  <div class="base-line" :class="head.class">
    <div v-if='head.readonly'>
      <span>{{head.prefix}}</span>
      <span class="readonly-info" >{{row[head.name]}}</span>
      <span>{{head.suffix}}</span>
    </div>
    <div  v-else  class="form-inline">
      <slot name="inputbody">
        <el-input v-model="row[head.name]" size="small" :placeholder="head.placeholder"
                  :id="'id_'+head.name" :name="head.name"
                  :maxlength="head.maxlength">
          <template v-slot:prepend >
            <span  v-if="head.prefix" v-html="head.prefix"></span>
          </template>
          <template v-slot:append>
            <span  v-if="head.suffix" v-html="head.suffix"></span>
          </template>
        </el-input>
      </slot>

    </div>
  </div>
</template>
<script>
export default {
  props:['row','head'],
  mounted(){
    if(this.head.css){
      ex.append_css(this.head.css)
    }
    if(this.head.mounted_express){
      ex.eval(this.head.mounted_express,{vc:this})
    }
  },
}
</script>