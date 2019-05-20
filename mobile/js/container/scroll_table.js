Vue.component('com-ctn-scroll-table',{
    props:['ctx'],
    template:`<div class="com-ctn-scroll-table">
              <cube-scroll :data="rows" ref="scroll"  :options="scrollOptions" @pulling-down="onPullingDown"
                  @pulling-up="onPullingUp">
            <component :is="table_editor" :heads="heads" :rows="childStore.rows" :option="table_option" @select="open_detail($event)"></component>
            <div v-if="childStore.rows.length == 0 " class="center-vh">暂无数据</div>
    </cube-scroll>
    </div>`,
    data(){
        var childStore = new Vue(table_store)
        childStore.rows=[]
        childStore.vc = this
        childStore.director_name = this.ctx. director_name
        table_option['nextlevel'] = this.ctx.detail_editor? true:false
        return {
            rows:this.childStore.rows,
            search_args: this.ctx.search_args || {},
            table_editor:this.ctx.table_editor || '',
            scrollOptions: {
                /* lock x-direction when scrolling horizontally and  vertically at the same time */
                directionLockThreshold: 0,
                click:true,
                pullDownRefresh:{
                    txt:'刷新成功!',
                },
                pullUpLoad:{
                    txt:{ more: '', noMore: '没有更多了!' }
                },
//                        preventDefaultException:{className:/(^van-cell$)/},
//                        preventDefault:false,
            },
        }
    },
    onPullingUp(){
        this.childStore.addNextPage().then(()=>{
            this.$refs.scroll.forceUpdate()
        })
    },
    onPullingDown(){
        this.childStore.search().then(()=>{
            this.$refs.scroll.forceUpdate()
        })
    },
})