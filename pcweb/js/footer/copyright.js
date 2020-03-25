require('./styl/copyright.styl')

Vue.component('com-ft-copyright',{
    props:['ctx'],
    template:`<div class="com-ft-copyright">
    <div class="web-wrap">
        <div v-text="ctx.copyright"></div>
    </div>
    </div>`
})

//wow bounceInUp