<template>
  <div class="tab-widget" :class="type" >
    <component v-if="top_editor" :is="top_editor"
               v-bind="top_ctx"
               :par_row="ctx.par_row"></component>


    <el-tabs class="active-tab-hightlight-top"  v-if="ctx.tabs.length >1 || type!='tab-full'" :type="my_el_type"
             @tab-click="handleClick"
             :value="ctx.crt_tab_name" >

      <!--<el-tab-pane v-for="tab in normed_tab( tabgroup.tabs )"            @mouseenter="set_hover(tab,true)" @mouseleave="set_hover(tab,false)"-->
      <el-tab-pane v-for="tab in normed_tab"
                   lazy
                   :key="tab.name"
                   :name="tab.name">
                        <span slot="label" v-if="tab.icon_image" class="tab-label" :class="{active:ctx.crt_tab_name==tab.name}">
                             <img class="icon_image_active" :src="tab.icon_image_active || tab.icon_image" alt="">
                             <img class="icon_image" :src=" tab.icon_image" alt="">
                            <span v-text="tab.label"></span>
                        </span>
        <span slot="label" v-else  v-text="tab.label" ></span>
        <!--<span v-if="!tab._loaded"></span>-->
        <transition name="fade">
          <component v-show="ctx.crt_tab_name==tab.name" :is="tab.editor || tab.com " :tab_head="tab"
                     :par_row="ctx.par_row"
                     :ref="'_tab_'+tab.name" @tab-event="up_event($event)"></component>
        </transition>

      </el-tab-pane>
    </el-tabs>

<!--     只有一个tab的时候，不用显示在el-tabs里面了。-->
    <component v-else v-for="tab in ctx.tabs"  :is="tab.editor || tab.com " :tab_head="tab"
               :par_row="ctx.par_row"
               :ref="'_tab_'+tab.name" @tab-event="up_event($event)"></component>
  </div>
</template>
<script>
export default {
  props:{
    ctx:{},
    type:{
      default:'tab-full'
    },
    top_editor:{},
    top_ctx:{},
  },
  data(){
    //ex.each(this.ctx.tabs,tab=>{
    //    if(tab.lazy_init){
    //        Vue.set(tab,'_loaded',false)
    //    }
    //})
    var childStore = new Vue()
    childStore.vc = this
    childStore.name='com-widget-el-tab'
    return {
      childStore:childStore,
      is_mounted:false,

    }
  },
  watch:{
    //'ctx.crt_tab_name':function (v){
    //     this.show_tab(v)
    // }
  },
  mounted:function(){
    this.is_mounted  = true
    // this.show_tab(this.ctx.crt_tab_name)

  },
  computed:{
    my_el_type(){
      if(this.type=='tab-full'){
        return 'border-card'
      }else if(this.type=='tab-v'){
        return 'card'// 'border-card' //
      }
    },
    normed_tab:function(){
      var tabs = this.ctx.tabs
      var par_row = this.ctx.par_row
      var out_tabs = ex.filter(tabs,function(tab){
        if(tab.show_express){
          return ex.eval(tab.show_express,{par_row:par_row})
          //return ex.boolExpress(par_row,tab.show)
        }else{
          return true
        }
      })
      return out_tabs
    }
  },
  methods:{
    setCurrentTab(tabname){
      this.ctx.crt_tab_name = tabname
    },
    set_hover(tab,value){
      Vue.set(tab,'_hover',value)
    },
    // show_tab(name){
    //   this.ctx.crt_tab_name=name
    // },
    handleClick(tab, event) {
      if(this.crt_tab_name != tab.name){
        // this.show_tab(tab.name)
        this.setCurrentTab(tab.name)
        this.$emit('click-tab',name)
      }
    },
    up_event:function(event){
      this.$emit('win-event',event)
    }
  }
}
</script>
<style scoped lang="scss">
.tab-label{
  img{
    height: 20px;
    width: auto;
    position: relative;
    top: -1px;
  }
  .icon_image{
    display: inline;
  }
  .icon_image_active{
    display: none;
  }
  &.active{
    .icon_image{
      display: none;
    }
    .icon_image_active{
      display: inline;
    }
  }
}

// 可能需要deep
.el-tabs--border-card>.el-tabs__header .el-tabs__item:not(.is-disabled):hover{
  .icon_image{
    display: none;
  }
  .icon_image_active{
    display: inline;
  }
}

.tab-v{
  background-color: white;
  .active-tab-hightlight-top{

    margin:0 20px;
    //border-left: 1px solid #e1e1e1;
    box-sizing: border-box;
    position: relative;
    min-height: 86vh; // 给一个min-height，保证切换tab时不会抖动太厉害。（由于每个tab页高度不一致，切换到height小的页面，滚动条会缩回去，造成抖动。）
    //padding: 20px;
  }
}

.tab-full{
  position: absolute;
  bottom: 0;top: 0;left: 0;right: 0;
  .active-tab-hightlight-top{
    width: 100%;
    height: 100%;
  }
  /deep/{
    .el-tabs{
      display: flex;
      flex-direction: column;
      height: 100%;
      .el-tabs__content{
        flex-grow:10;
        position: relative;
        overflow: auto;
      }
    }

    .active-tab-hightlight-top{
      &>.el-tabs__header{
        .el-tabs__item {
          &.is-top.is-active{
            color: #3e8ebd;
          }
          &.is-top.is-active:after{
            content: '';
            display: block;
            position: absolute;
            top:0;
            left: 0;
            right:0;
            width: 100%;
            height: 3px;
            background-color: #3e8ebd;
          }
        }
      }
    }
  }


}

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}

</style>