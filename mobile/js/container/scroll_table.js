Vue.component('com-ctn-scroll-table',{
    props:['ctx'],
    template:`<div class="com-ctn-scroll-table">
              <cube-scroll :data="parStore.rows" ref="scroll"  :options="scrollOptions" @pulling-down="onPullingDown"
                  @pulling-up="onPullingUp">
            <component :is="table_editor" :heads="ctx.heads" :rows="parStore.rows"></component>
            <div v-if="parStore.rows.length == 0 " class="center-vh">
                <van-icon name="search" size='1rem' color="#c9c9c9" />
            </div>
    </cube-scroll>
    </div>`,
    data(){
        var parStore = ex.vueParStore(this)
        //table_option['nextlevel'] = this.ctx.detail_editor? true:false
        return {
            parStore:parStore,
            table_editor:this.ctx.table_editor || 'com-ctn-table-van-cell',
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
    methods:{
        onPullingUp(){
            this.parStore.addNextPage().then(()=>{
                this.$refs.scroll.forceUpdate()
            })
        },
        onPullingDown(){
            this.parStore.search().then(()=>{
                this.$refs.scroll.forceUpdate()
            })
        },

    }

})