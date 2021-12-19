<template>
  <div :class="['com-field-minute','field-'+head.name,head.class]" >
    <input v-if="!head.readonly" type="text" style="display: none"
           :id="'id_'+head.name"
           :name="head.name"
           v-model="row[head.name]">

    <el-time-picker
        v-model="row[head.name]"
        value-format="HH:mm"
        size="small"
        :placeholder="head.placeholder || '请输入时间'">
    </el-time-picker>
  </div>
</template>
<script>
export  default  {
  props:['row','head'],
  computed:{
    innvalue(){
      return this.row[this.head.name]
    }
  },
  watch:{
    innvalue(v){
      if(v.length > 10){
        this.row[this.head.name] = v.slice(11)
      }else{
        this.row[this.head.name] = v
      }
    }
  },
  mounted(){
    if(this.head.css){
      ex.append_css(this.head.css)
    }
  },
}
</script>

Vue.component('com-field-time',time_field)