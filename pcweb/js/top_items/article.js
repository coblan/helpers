require('./styl/article.styl')

Vue.component('com-ti-article',{
    props:['ctx'],
    template:`<div class="com-ti-article" :class="ctx.class">
    <div class="title" v-text="ctx.row.title"></div>
    <div v-html="ctx.row.content"></div>
    </div>`,

})