require('./styl/live_list.styl')

var live_list={
    props:['ctx'],
    basename:'live-list',
    template:`<div class="com-live-list">
        <com-uis-nav-bar :title="ctx.title" :back="can_back" :ops="ctx.ops"></com-uis-nav-bar>
       <cube-scroll :data="childStore.rows" ref="scroll"  :options="scrollOptions" @pulling-down="onPullingDown"
                  @pulling-up="onPullingUp">
            <component :is="table_editor" :heads="ctx.heads" :rows="childStore.rows"  @select="triggerBlockClick($event)"></component>
            <div v-if="childStore.rows.length == 0 " class="center-vh">暂无数据</div>
    </cube-scroll>
    </div>`,
    data(){
        var childStore = new Vue(table_store)
        childStore.rows= this.ctx. rows || []
        childStore.vc = this
        childStore.director_name = this.ctx.director_name

        return {
            childStore:childStore,
            table_editor: this.ctx.table_editor || 'com-ctn-table-van-cell',
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

            },
        }
    },
    mounted(){
        if(this.ctx.rows.length==0){
            this.childStore.search()
        }
    },
    computed:{
        can_back(){
            return this.$root.stack.length >1
        }
    },
    methods:{
        triggerBlockClick(row){
            if(this.ctx.block_click){
                ex.eval(this.ctx.block_click,{row:row,ps:this.childStore})
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
    }
}

Vue.component('com-list-list',live_list)

window.live_list = live_list