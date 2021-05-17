<template>
    <div class="com-live-list" >
        <com-uis-nav-bar v-if="is_page" :title="ctx.title" :back="can_back" :ops="ctx.ops"></com-uis-nav-bar>

        <pull_list ref="pull_list" :ctx="ctx" :passive="true"></pull_list>

        <div v-if="ctx.footer" class="footer-content">
            <component :is="ctx.footer.editor"  :ctx="ctx.footer"></component>
        </div>

    </div>
</template>
<script>
import pull_list from '../container/pull_list.vue'

export default {
    props:['ctx'],
    basename:'live-list',
    components:{
        pull_list
    },
    mounted(){
        Vue.nextTick(()=>{
            this.init()
        })
    },
    update(){

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

// TODO:经过修改后，只导出了com-live-list, 不知道com-list-list是否还有用！
//Vue.component('com-list-list',live_list)
//Vue.component('com-live-list',live_list)
</script>
<style scoped lang="scss">
    .com-live-list{
        display:flex;
        flex-direction: column;
        background-color: #f8f8f8;
        height: 100%;
        .van-list{
            flex-grow :10;
            overflow: auto;
            -webkit-overflow-scrolling: touch;
        }
        .list-content{
            min-height: 100%;
        }

    }

</style>


