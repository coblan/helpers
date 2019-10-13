require('./styl/live_swip_tab.styl')

window.live_swip_tab = {
    props:['ctx'],
    basename:'live-swip-tab',
    template:`<div class="live-swip-tab flex-v">
    <!--<div class="title-block">产品服务</div>-->
    <com-uis-nav-bar :title="ctx.title" :back="can_back" ></com-uis-nav-bar>
    <div style="height: .2rem"></div>
    <cube-tab-bar v-model="selectedLabel" show-slider :use-transition="false" ref="tabNav" :data="tabLabels">
    </cube-tab-bar>

    <div  class="tab-slide-container">
        <cube-slide
            ref="slide"
            :loop="false"
            :initial-index="initialIndex"
            :auto-play="false"
            :show-dots="false"
            :allowVertical="true"
            :options="slideOptions"
            :refreshResetCurrent="false"
            @scroll="scroll"
            @change="changePage"
        >
            <!-- 关注 -->
            <cube-slide-item v-for="(head,index) in ctx.heads">
                <component :key="index" v-if="is_loaded(index)" :is="head.editor" :ctx="head" ></component>
                <div v-else style="height: 400px"></div>
                <!--<div class="scroll-list-wrap dyn-resize" data-size-express="'height:calc('+ scope.winheight+'px - 1rem )'">-->
                    <!--<cube-scroll :data="device_list" :options="scrollOptions">-->
                    <!--<com-goods-list :goods-list="device_list"></com-goods-list>-->
                    <!--</cube-scroll>-->
                <!--</div>-->
            </cube-slide-item>
        </cube-slide>
    </div>
    </div>`,
    data(){
        return {
            loaded_tab:[],
            selectedLabel:this.ctx.heads[0].label,
            tabLabels:this.ctx.heads,
            slideOptions: {
                listenScroll: true,
                probeType: 3,
                /* lock y-direction when scrolling horizontally and  vertically at the same time */
                directionLockThreshold: 0
            },
            scrollOptions: {
                /* lock x-direction when scrolling horizontally and  vertically at the same time */
                directionLockThreshold: 0,
                click:false
            },
        }
    },
    mounted(){
        if(this.ctx.css){
            ex.append_css(this.ctx.css)
        }
        if(this.ctx.init_express){
            ex.eval(this.ctx.init_express,{self:this})
        }
    },
    activated(){
        //alert('active')
        setTimeout(()=>{
            this.$refs.slide.refresh()
        },200)
    },
    computed: {
        //tabLabels(){
        //    return  ex.map(this.ctx.heads,(head)=>{
        //        return head.label
        //    })
        //},
        initialIndex () {
            let index = 0
            let label_list = this.tabLabels.map(item=>item.label)
            index = label_list.indexOf(this.selectedLabel)
            Vue.nextTick(()=>{
                this.loaded_tab.push(index)
            })
            return index
        },
        can_back(){
            return this.$root.stack.length >1
        },
    },
    methods:{
        is_loaded(index){
            return ex.isin(index,this.loaded_tab)
        },
        changePage (current) {
            if(! ex.isin(current,this.loaded_tab)){
                Vue.nextTick(()=>{
                    this.loaded_tab.push(current)
                })
            }
            this.selectedLabel = this.tabLabels[current].label
            console.log(current)
        },
        scroll (pos) {
            const x = Math.abs(pos.x)

            //var tabItemWidth = 0
            //ex.each($(this.$refs.tabNav.$el).find('.cube-tab'),(item)=>{
            //    tabItemWidth += $(item).outerWidth()
            //})

            //tabItemWidth = Math.min(tabItemWidth, this.$refs.tabNav.$el.clientWidth)
            const tabItemWidth = this.$refs.tabNav.$el.clientWidth
            const slideScrollerWidth = this.$refs.slide.slide.scrollerWidth
            const deltaX = x / slideScrollerWidth * tabItemWidth
            this.$refs.tabNav.setSliderTransform(deltaX)
        },
    }
}