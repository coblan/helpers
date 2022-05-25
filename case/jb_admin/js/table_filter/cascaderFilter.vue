<template>
  <div class="com-filter-cascasder">
    <el-cascader
        :show-all-levels="false"
        v-model="search_args[head.name]"
        :options="head.options"
        :placeholder="head.label"
        :props="myprops"
        @change="onChange"
        size="small"
        clearable>
    </el-cascader>
  </div>
</template>
<script>
export  default  {
  props:['head','search_args'],
  computed:{
    myprops(){
      if(this.head.onlyLeaf){
        return  {emitPath:false}
      }else{
        return {checkStrictly: true,emitPath:false }
      }
    }
  },
  methods:{
    onChange(){
      if(!this.search_args[this.head.name]){
        delete this.search_args[this.head.name]
      }
    }
  }
}
</script>

