require('./styl/article_simple.styl')

Vue.component('com-li-article-simple',{
    props:['ctx'],
    template:`<div class="com-li-article-simple">
    <img :src="ctx.cover" alt="">
    <div class="content">
        <span class="title" :class="{clickable:has_action}" v-text="ctx.title" @click="on_click()"></span>
    </div>
    </div>`,
    data(){
        return {
            parStore:ex.vueParStore(this)
        }
    },
    computed:{
        has_action(){
            if(this.parStore.vc.ctx.action){
                return true
            }else{
                return false
            }
        }
    },
    methods:{
        on_click(){
            var action= this.parStore.vc.ctx.action
            if(action){
                ex.eval(action,{row:this.ctx})
            }
        }
    }
})