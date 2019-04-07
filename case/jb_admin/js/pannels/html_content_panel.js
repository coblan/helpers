require('./scss/html_content_panel.scss')

var html_panel={
    props:['ctx'],
    template:`<div class="com-html-content-panel" v-html="ctx.content"></div>`,


}
Vue.component('com-html-content-panel',html_panel)