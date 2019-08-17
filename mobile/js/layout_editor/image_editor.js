require('./styl/image_editor.styl')

Vue.component('com-live-layout-image',{
    props:['ctx'],
    template:`<div class="com-live-layout-image">
        <img :src="ctx.src" alt="">
    </div>`
})