require('./scss/ifram_panel.scss')

var iframe_panel={
    props:['ctx'],
    template:`<div class="com-iframe-panel">
        <iframe :src="ctx.url" style="width: 100%;height:100%;vertical-align:top" scrolling="auto"></iframe>
    </div>`,



}
Vue.component('com-iframe-panel',iframe_panel)