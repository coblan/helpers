require('./styl/block_ctn.styl')

Vue.component('com-top-block-ctn',{
    props:['ctx'],
    template:`<div class="com-top-block-ctn">
        <div class = 'web-wrap'>
        <div v-if="ctx.title" class="title" v-text="ctx.title"> </div>
        <div v-if="ctx.sub_title" class="sub-title" v-text="ctx.sub_title"></div>
        <div class="block-content">
          <component v-for="item in ctx.items" :is="item.editor" :ctx="item"></component>
        </div>
        </div>
    </div>`
})