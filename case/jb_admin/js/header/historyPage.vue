<template>

     <div class="history-page">
<!--       <el-tag-->
<!--           v-for="page in pagelist"-->
<!--           :key="page.name"-->
<!--           closable-->
<!--           effect="plain"-->
<!--           size="small"-->
<!--           :disable-transitions="false"-->
<!--           @close="handleClose(tag)">-->
<!--         {{page.label}}-->
<!--       </el-tag>-->
       <span title="最近访问历史">
         <i class="fa fa-history toggle-button"

            :class="{active:show_history}" @click="show_history = !show_history" aria-hidden="true"></i>
       </span>

       <div class="wrap" v-for="page in pagelist" v-if="show_history">
         <div class="page-label clickable" :class="{active:page.name==current_name}"  @click="goto(page)">{{page.label}}</div>
         
<!--         <i class="fa fa-lock" aria-hidden="true"></i>-->
       </div>

      </div>


</template>
<script>
export default {
  props:['ctx'],
  data(){
    var show_history = ex.defaultGet(this.ctx.show_history,true)
    var show_history = ex.localGet('_history-page.show',show_history)
    return {
        show_history:show_history,
        pagelist:[],
        current_name:page_name,
    }
  },
  mounted(){
    this.updatePageList()
  },
  watch:{
    show_history(nv){
      ex.localSet('_history-page.show',nv)
    }
  },
  methods:{
    handleClose(){

    },
    updatePageList(){
      var pp_str = localStorage.getItem('_history-page')
      if(pp_str){
        var pp = JSON.parse(pp_str)
      } else{
        var pp = []
      }
      var one = ex.findone(pp,{name:page_name})
      if(one){
        // 不断的把老的历史 放到最前面
        var index = pp.indexOf(one)
        pp.splice(index,1)
        pp.splice(0,0,one)
      }else{
        if(page_name){
          pp.splice(0,0, {href:location.href,label:page_label,name:page_name})
        }
      }
      if(pp.length>5){
        pp.pop()
      }
      this.pagelist  = pp
      localStorage.setItem('_history-page',JSON.stringify(this.pagelist))
    },
    goto(page){
      location=page.href
    }
  }
}
</script>
<style scoped lang="scss">
.history-page{
  display:  inline-block;
  padding: 15px 0;
  //background-color: #252f34;
  //background-color: white;
}
.wrap{
  display: inline-block;
  margin-right: 10px;

}
.page-label{
    display: inline-block;
    //color: #8aa4af;
    color: #dcdcdc;
    font-size: 80%;
    position: relative;
    &.active,&:hover{
      color: white;
      &:after{
        content: '';
        position: absolute;
        left: 0;
        right: 0;
        bottom: -5px;
        height: 1px;
        background-color: white;
      }
    }
  &.active{
    font-size: 90%
  }
}
.toggle-button{
  color:#8aa4af;
  cursor: pointer;
  margin-right: 3px;
  &.active{
    color: white;
  }
}

</style>