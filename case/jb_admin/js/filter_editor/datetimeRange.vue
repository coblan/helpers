<template>
  <div  class="com-filter-datetime-range flex flex-ac">
    <span v-text="head.label" style="white-space: nowrap"></span>:
    <!--<input class="start form-control input-sm " v-model="start" readonly-->
    <!--style="background-color: white;width: 12em"-->
    <!--placeholder="开始时间">-->
    <slot name="start-input"  v-bind:heads="heads">
      <com-field-datetime :head="heads[0]" :row.sync="search_args"></com-field-datetime>
    </slot>

    <div style="display: inline-block;margin: 0 2px;" >-</div>
    <slot name="end-input"  v-bind:heads="heads">
      <com-field-datetime :head="heads[1]" :row.sync="search_args"></com-field-datetime>
    </slot>

    <!--<input class="end form-control input-sm"  v-model="end"  readonly-->
    <!--style="background-color: white;width: 12em"-->
    <!--placeholder="结束时间">-->
  </div>
</template>
<script>
export default {
  props:['head','search_args'],
  data:function(){
//var start=this.search_args['_start_'+this.head.name]
//var end=this.search_args['_end_'+this.head.name]
    return {
      heads:[
        {name:'_start_'+this.head.name,placeholder:cfg.tr('开始时间'),clearable:this.head.clearable,width:this.head.width},
        {name:'_end_'+this.head.name,placeholder:cfg.tr('结束时间'),clearable:this.head.clearable,width:this.head.width}
      ]
    }
  },
  computed:{
    start(){
      return this.search_args['_start_'+this.head.name]
    },
    end(){
      return this.search_args['_end_'+this.head.name]
    }
  },
  watch:{
    start:function(nv,ov){
      if(nv && this.end){
        if(nv>this.end){
          cfg.showError('开始时间必须小于结束时间')

//this.search_args['_start_'+this.head.name] = ov
          this.$nextTick(()=>{
            Vue.set(this.search_args,'_start_'+this.head.name,ov)
          })

        }
      }
//Vue.set(this.search_args,'_start_'+this.head.name,nv)

    },
    end:function(nv,ov){
      if(nv && this.start){
        if(nv<this.start){
          cfg.showError('结束时间必须大于开始时间')
          this.$nextTick(()=>{
            Vue.set(this.search_args,'_end_'+this.head.name,ov)
          })

//var self=this
//Vue.nextTick(function(){
//    self.end = ov
//})
//return
        }
      }
//Vue.set(this.search_args,'_end_'+this.head.name,nv)

    }
  },
}
</script>

<style scoped lang="scss">
//.com-filter-datetime-range{
//  background-color: red;
//}
.com-filter-datetime-range{
  ::v-deep{
    .el-input__inner{
      width: 182px
    }
  }
}


</style>