
var html_panel={
    props:['ctx'],
    template:`<div class="com-html-panel" v-html="ctx.content"></div>`,


}
Vue.component('com-html-panel',html_panel)