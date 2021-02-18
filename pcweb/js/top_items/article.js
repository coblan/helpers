require('./styl/article.styl')

Vue.component('com-ti-article',{
    props:['ctx'],
    template:`<div class="com-ti-article" :class="ctx.class">
    <div class="title" v-text="ctx.row.title"></div>
    <div class="article-content" v-html="ctx.row.content"></div>
    </div>`,
    mounted(){
        if(this.ctx.mounted_express){
            ex.eval(this.ctx.mounted_express,{vc:this,head:this.ctx})
        }
    }
})