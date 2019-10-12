require('./styl/live_list.styl')

var live_list={
    props:['ctx'],
    basename:'live-list',
    template:`<div class="com-live-list" :class="ctx.class">
        <com-uis-nav-bar v-if="is_page" :title="ctx.title" :back="can_back" :ops="ctx.ops"></com-uis-nav-bar>
       <!--<cube-scroll :data="childStore.rows" ref="scroll"  :options="scrollOptions" @pulling-down="onPullingDown"-->
                  <!--@pulling-up="onPullingUp">-->
            <!--<component :is="table_editor" :heads="ctx.heads" :rows="childStore.rows"  @select="triggerBlockClick($event)"></component>-->
            <!--<div v-if="childStore.rows.length == 0 " class="center-vh">暂无数据</div>-->
    <!--</cube-scroll>-->


    <van-list
      v-model="loading"
      :finished="finished"
      finished-text="没有更多了"
      :immediate-check="false"
      @load="onLoad"
    >
    <van-pull-refresh v-model="freshing" @refresh="onRefresh">
        <component class="content-wrap" :is="table_editor" :heads="ctx.heads" :rows="childStore.rows"  @select="triggerBlockClick($event)"></component>
    </van-pull-refresh>
    </van-list>



    </div>`,
    data(){
        var childStore = new Vue(table_store)
        childStore.rows= this.ctx. rows || []
        childStore.vc = this
        childStore.director_name = this.ctx.director_name
        if(this.ctx.search_args){
            ex.vueAssign(childStore.search_args,this.ctx.search_args)
        }

        return {
            freshing:false,
            loading:false,
            finished:false,
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
        if(this.ctx.css){
            ex.append_css(this.ctx.css)
        }
        if(this.ctx.init_express){
            ex.eval(this.ctx.init_express,{self:this,cs:this.childStore})
        }else  if(!this.ctx.rows || this.ctx.rows.length==0){
            this.childStore.search()
        }
    },
    computed:{
        is_page(){
            if(this.ctx.is_page ==undefined){
                return true
            }else{
                return this.ctx.is_page
            }

        },
        can_back(){
            return this.$root.stack.length >1
        }
    },
    methods:{
        onRefresh(){
            console.log('刷新')
            this.childStore.search().then(()=>{
                this.freshing = false
                this.finished=false
            })

        },
        onLoad(){
            console.log('加载')
            this.childStore.addNextPage().then(()=>{
                this.loading = false
                if(this.childStore.search_args._page * this.childStore.row_pages.perpage >=  this.childStore.row_pages.total   ){
                    this.finished=true
                }else{
                    this.finished=false
                }
            })
        },
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
    },
    deactivated(){
        this.scroll = $(this.$el).find('.van-list').scrollTop()
    },
    activated() {
        if( this.scroll){
            var count =0
            var index =  setInterval(()=>{
                $(this.$el).find('.van-list').scrollTop( this.scroll)
                count+=30
                if(count > 160){
                    clearInterval(index)
                }
            },30)
        }
    },
}

Vue.component('com-list-list',live_list)
Vue.component('com-live-list',live_list)

window.live_list = live_list