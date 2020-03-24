require('./styl/msg_panel.styl')

Vue.component('com-ti-msg-panel',{
    props:['ctx'],
    template:`<div class="com-ti-msg-panel" :class="ctx.class">
    <div class="title" v-text="ctx.title"></div>
    <div class="content" v-html="ctx.content"></div>
    </div>`,

})