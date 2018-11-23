
var iframe_panel={
    props:['ctx'],
    template:`<iframe class="com-html-panel" :src="ctx.url" style="width: 100%;height:100% " scrolling="auto"></iframe>`,



}
Vue.component('com-iframe-panel',iframe_panel)