Vue.component('com-slide-iframe',{
    props:['ctx'],
    template:`<iframe :src="ctx.url" style="width:100%;height: 100%;"></iframe>`,
})