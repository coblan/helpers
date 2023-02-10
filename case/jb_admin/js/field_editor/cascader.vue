<template>
  <div class="com-field-cascader" :style="{'--width':this.head.width}">
<!--    <span v-if="head.readonly">{{label}}</span>-->
<!--    <template v-else>-->
      <input v-if="!head.readonly" type="text" style="display: none" :id="'id_'+head.name" :name="head.name" v-model="row[head.name]">
      <el-cascader class="com-field-cascader"
                   :disabled="head.readonly"
                   v-model="row[head.name]"
                   :options="head.options"
                   :show-all-levels="head.showAllLevels"
                   :filterable="head.filterable"
                   :props="myprops"
                   size="small"
                   clearable>
      </el-cascader>
<!--    </template>-->
  </div>
</template>
<script>
export  default {
  props:['row','head'],
  data(){
    return {
      selected:[1,2],
// demon 数据
      options: [{
        value:'1',
        label: '一级 1',
        children: [{
          value:'21',
          label: '二级 1-1',
          children: [{
            value:'31',
            label: '三级 1-1-1',
            children:[
              {
                value:'41',
                label:'四级1'
              }
            ]
          }]
        }]
      }, {
        value:'2',
        label: '一级 2',
        children: [{
          value:'22',
          label: '二级 2-1',
          children: [{
            value:'32',
            label: '三级 2-1-1',
            pk:3
          }]
        }, {
          value:'23',
          label: '二级 2-2',
          children: [{
            value:'33',
            label: '三级 2-2-1'
          }]
        }]
      },
      ],
    }
  },
//default-expand-all
  computed:{
  label:function(){
    return this.row['_'+this.head.name+'_label']
  },
  myprops(){
    var dc = {}
    if(this.head.multiple){
      dc.multiple=true
    }
    if(this.head.onlyLeaf){
      dc.emitPath = false
    }else{
      Object.assign(dc, {checkStrictly: true,emitPath:false })
    }
    return dc
  }
}
}
</script>
<style scoped lang="scss">
.com-field-cascader{
    ::v-deep{
      input{
        width: var(--width);
        //width: 50rem;
      }
    }
}
</style>