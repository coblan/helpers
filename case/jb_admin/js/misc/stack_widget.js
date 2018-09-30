require('./scss/stack_widget.scss')

Vue.component('com-widget-stack',{
    props:['ctx_list'],
    template:`<div class="com-widget-stack">
        <component v-for="(ctx,index) in ctx_list" v-show="index==ctx_list.length-1"   :is="ctx.widget" :ctx="ctx"></component>
    </div>`,


})