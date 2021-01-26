require('./styl/lay_main_small.styl')

Vue.component('com-top-lay-main-small',{
    props:['ctx'],
    template:`<div class="com-top-lay-main-small">
    <div class="web-wrap">
        <div class="main">
            <component :is="item.editor"  :key="item.pk || item.id || item.name" v-for="item in ctx.main_items" :ctx="item"></component>
        </div>
        <div class="small">
            <component :is="item.editor" :key="item.pk || item.id || item.name" v-for="item in ctx.small_items" :ctx="item"></component>
        </div>
    </div>
    </div>`
})