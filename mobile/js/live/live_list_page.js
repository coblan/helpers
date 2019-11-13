require('./styl/live_list_page.styl')

var live_list_page ={
    /*
    *  与live_list 获取数据一致，但是具备上一页，下一页，以及 总数功能
    *
    * */
    props:['ctx'],
    basename:'live-list-page',
    template:`<div class="com-live-list-page">
        <com-uis-nav-bar :title="ctx.title" :back="can_back" :ops="ctx.ops"></com-uis-nav-bar>
            <!--<cube-scroll :data="childStore.rows" ref="scroll"  :options="scrollOptions" @pulling-down="onPullingDown"-->
                  <!--@pulling-up="onPullingUp">-->
              <div class="middle-wrap">
                <component :is="table_editor" :heads="ctx.heads" :rows="childStore.rows"  @select="on_block_click($event)"></component>
              </div>

            <div v-if="childStore.rows.length == 0 " class="center-vh">暂无数据</div>
    <!--</cube-scroll>-->
    <div class="footer">
        <van-pagination
              v-model="childStore.row_pages.crt_page"
              :total-items="childStore.row_pages.total"
              :items-per-page="childStore.row_pages.perpage"
              @change="childStore.search_args._page = childStore.row_pages.crt_page; childStore.getRows()"
              mode="simple">
              </van-pagination>
          <span class="total-count" >共<span v-text="childStore.row_pages.total"></span>条</span>
  </div>
    </div>`,
    data(){
        var childStore = new Vue(table_store)
        childStore.rows= this.ctx. rows || []
        childStore.vc = this
        childStore.director_name = this.ctx.director_name
        childStore.row_pages = this.ctx.row_pages

        return {
            currentPage:1,
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
    computed:{
        can_back(){
            return this.$root.stack.length >1
        }
    },
    methods:{
        on_block_click(row){
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

Vue.component('com-list-list-page',live_list_page)

window.live_list_page = live_list_page