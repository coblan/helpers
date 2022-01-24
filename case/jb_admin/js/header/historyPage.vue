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
       <i class="fa fa-history toggle-button" :class="{active:show_history}" @click="show_history = !show_history" aria-hidden="true"></i>
       <div class="wrap" v-for="page in pagelist" v-if="show_history">
         <div class="page-label clickable" :class="{active:page.name==current_name}"  @click="goto(page)">{{page.label}}</div>
         
<!--         <i class="fa fa-lock" aria-hidden="true"></i>-->
       </div>

      </div>


</template>
<script>
export default {
  data(){
    return {
        show_history:true,
        pagelist:[],
        current_name:page_name,
    }
  },
  mounted(){
    this.updatePageList()
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
        // var index = pp.indexOf(one)
        // pp.splice(index,1)
        // pp.splice(0,0,one)
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
}
.wrap{
  display: inline-block;
  margin-right: 10px;
}
.page-label{
    display: inline-block;
    color: #b4abab;
}
.toggle-button{
  color:grey;
  &.active{
    color: white;
  }
}
.active{
  color: white;
}
</style>