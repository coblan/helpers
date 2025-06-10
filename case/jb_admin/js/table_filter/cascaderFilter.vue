<template>
  <div class="com-filter-cascasder">
    <el-cascader
        v-if="head.append_to_body==undefined"
        :style="{width:head.width}"
        :show-all-levels="head.show_all_level==undefined?false:head.show_all_level "
        v-model="search_args[head.name]"
        :options="head.options"
        :placeholder="head.label"
        :props="myprops"
        @change="onChange"
        :popper-class="head.pop_class"
        size="small"
        :filterable="head.filterable"
        clearable>
    </el-cascader>
    <el-cascader
        v-else
        :style="{width:head.width}"
        :show-all-levels="head.show_all_level==undefined?false:head.show_all_level "
        v-model="search_args[head.name]"
        :options="head.options"
        :placeholder="head.label"
        :props="myprops"
        @change="onChange"
        :popper-class="head.pop_class"
        size="small"
        :filterable="head.filterable"
        :append-to-body="head.append_to_body"
        :popper-options="popperOptions"
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
  data(){
    return {
      popperOptions:{
              // 核心：调整定位修饰符，确保全屏时正确计算位置
              modifiers: {
                // 禁用溢出限制，允许下拉框超出容器
                preventOverflow: {
                  enabled: false
                },
                // 调整定位偏移，避免被遮挡
                offset: {
                  offset: '0, 8px' // 垂直偏移8px
                },
                // 强制使用固定定位，避免全屏时定位错乱
                computeStyle: {
                  gpuAcceleration: false,
                      transform: false
                }
              }

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

