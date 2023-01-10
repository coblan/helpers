<template>
  <com-backend-table class="com-tab-table" v-if="loaded"
                     ref="backend_table" :ctx="tab_head.table_ctx"></com-backend-table>
</template>
<script>

export default {
  props:['tab_head','par_row'],
  data(){
    var childStore = {
      vc:this,
      name:'com-tab-table'
    }
    return {
        childStore:childStore,
        loaded:false,
    }
  },
  computed:{
     proxy(){
       var self = this
       return new Proxy(this.$refs.backend_table,{
         get: function(obj, prop) {
           if(prop in self){
             return  self[prop]
           }else if(prop in obj){
             return  obj[prop]
           }else if(obj.proxy){
             return  obj.proxy[prop]
           }
         }
       })
     }
  },
  mounted(){
    // 去掉rows是为了防止第二次打开tab-table时，携带了上次的rows数据
    this.tab_head.table_ctx.rows=[]
    this.init_search_args()
  },
  methods:{
    init_search_args(){
      var search_args = {}
      if(this.tab_head.filter_express){
        search_args = ex.eval(this.tab_head.filter_express,{par_row:this.par_row,vc:this,ps:this.childStore})
      }else if(this.tab_head.pre_set){
        // pre_set 含义不够清晰，被 filter_express 替代了
        var pre_set = ex.eval(this.tab_head.pre_set,{par_row:this.par_row,vc:this,ps:this.childStore})
        ex.assign(search_args,pre_set)
      }
      ex.vueAssign(this.tab_head.table_ctx.search_args,search_args)
      this.loaded=true
    }
  }
}
</script>
<style scoped lang="scss">
.tab-full{
  .com-tab-table{
    position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 1em;
    //height: calc( var(--content-height) - 80px);
    //width: 100%;
  }
}
</style>