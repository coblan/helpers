Vue.component('com-top-html',{
    props:['ctx'],
    template:`<div class="com-top-html" :class="ctx.class">
    <div class="web-wrap" v-html="ctx.html"></div>
    </div>`,
    mounted(){
        if(this.ctx.css){
            ex.append_css(this.ctx.css)
        }
    }
})