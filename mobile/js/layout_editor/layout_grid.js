require('./styl/layout_grid.styl')

Vue.component('com-layout-grid',{
    props:['ctx'],
    template:`<div class="com-layout-grid">
        <component :is="head.editor" v-for="head in ctx.heads" :ctx="head"></component>
    </div>`
})

Vue.component('com-grid-icon-btn',{
    props:['ctx'],
    template:`<div class="grid-3" @click="on_click()">
     <img :src="ctx.icon" alt="">
     <div class="label" v-text="ctx.label"></div>
    </div>`,
    data(){
        return {
            parStore:ex.vueParStore(this)
        }
    },
    methods:{
        on_click(){
            ex.eval(this.ctx.action,{head:this.ctx,ps:this.parStore})
        }
    }
})