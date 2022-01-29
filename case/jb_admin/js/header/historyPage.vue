<template>

     <div class="history-page">
       <span title="最近访问历史">
               <el-popover
                   placement="top"
                   width="200"
                   trigger="click"
               >
<!--                trigger="hover"-->
               <div>
                 <h4>页面访问历史</h4>
                 <div class="setting-row" style="margin-top: 20px">
                   <span>启用</span>
                   <span>
                      <el-checkbox v-model="show_history"></el-checkbox>
                   </span>
                 </div>
                 <hr>
                <div class="setting-row" style="margin-top: 10px;margin-bottom: 10px; font-weight: bold;">
                  <span>页面</span>
                  <span>锁定</span>
                </div>
                 <div class="setting-row" v-for="page in pagelist">
                   <span>{{page.label}}</span>
                   <span>
                      <el-checkbox v-model="page.lock"></el-checkbox>
                   </span>
                 </div>
               </div>
                <span slot="reference">
                    <i class="fa fa-history toggle-button"
                       :class="{active:show_history}"  aria-hidden="true"></i>
                </span>

              </el-popover>


<!--         @click="show_history = !show_history"-->

       </span>

       <div class="wrap" v-for="page in pagelist" v-if="show_history">
<!--         <div class="page-label" :class="{active:page.name==current_name}">-->
           <a class="page-label" :class="{active:page.name==current_name,lock:page.lock}" :href="page.href">{{page.label}}</a>
<!--           </div>-->
         
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
    },
    pagelist:{
      deep:true,
      handler(nv){
          ex.localSet('_history-page',nv)
      }
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
        // var index = pp.indexOf(one)
        // pp.splice(index,1)
        // pp.splice(0,0,one)
      }else{
        if(page_name && page_label){
          pp.push({href:location.href,label:page_label,name:page_name})
          // pp.splice(0,0, {href:location.href,label:page_label,name:page_name})
        }
      }
      var locked = ex.filter(pp,{lock:true})

      if(pp.length - locked.length>4){
        // pp.pop()
        var overflow_count = (pp.length - locked.length) -4
        var p_length = pp.length
        var popindex = []
        for(var i= 0 ; i < pp.length;i++){
          if(overflow_count <=0){
            break
          }
          if(!pp[i].lock){
            popindex.push(i)
            overflow_count = overflow_count -1
          }
        }
        popindex = popindex.reverse()
        for(var i =0;i < popindex.length;i++){
          pp.splice(popindex[i],1)
        }
      }
      this.pagelist  = pp
      // localStorage.setItem('_history-page',JSON.stringify(this.pagelist))
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
    &.lock:after{
        content: '';
      display: block;
      background-color: white;
      width: 4px;
      height: 4px;
      border-radius: 2px;
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      bottom: -4px;
    }
    &.active,&:hover{
      color: white;
      &:after{
        content: '';
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 5px;
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
.setting-row{
  display: flex;
  justify-content: space-between;
}
</style>