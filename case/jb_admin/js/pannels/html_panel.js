require('./scss/html_panel.scss')

var html_panel={
    props:['ctx'],
    template:`<div class="con-html-panel" v-html="ctx.content"></div>`,


}
Vue.component('com-html-panel',html_panel)