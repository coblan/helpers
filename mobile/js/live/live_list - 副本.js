require('./styl/live_list.styl')
/*
* 类似于 pc的table组件
* 具备滚动加载功能
*
* */
export var live_list={
    props:['ctx'],
    basename:'live-list',
    template:`<div class="com-live-list" >
        <com-uis-nav-bar v-if="is_page" :title="ctx.title" :back="can_back" :ops="ctx.ops"></com-uis-nav-bar>
       <!--<cube-scroll :data="childStore.rows" ref="scroll"  :options="scrollOptions" @pulling-down="onPullingDown"-->
                  <!--@pulling-up="onPullingUp">-->
            <!--<component :is="table_editor" :heads="ctx.heads" :rows="childStore.rows"  @select="triggerBlockClick($event)"></component>-->
            <!--<div v-if="childStore.rows.length == 0 " class="center-vh">暂无数据</div>-->
    <!--</cube-scroll>-->


    <com-pull-list ref="pull_list" :ctx="ctx" :passive="true"></com-pull-list>

     <div v-if="ctx.footer" class="footer-content">
         <component :is="ctx.footer.editor"  :ctx="ctx.footer"></component>
     </div>

    </div>`,
    data(){
        return {
        }
    },
    mounted(){
       this.init()
    },
    computed:{
        //childStore(){
        //    return this.$refs.pull_list.childStore
        //    //if(this.$refs.pull_list){
        //    //    return this.$refs.pull_list.childStore
        //    //}else{
        //    //    return {}
        //    //}
        //},
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
        init(){
            this.childStore = this.$refs.pull_list.childStore
            if(this.ctx.css){
                ex.append_css(this.ctx.css)
            }
            if(this.ctx.init_express){
                ex.eval(this.ctx.init_express,{self:this,cs:this.childStore})
            }else  if(!this.ctx.rows || this.ctx.rows.length==0){
                this.childStore.search()
            }
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