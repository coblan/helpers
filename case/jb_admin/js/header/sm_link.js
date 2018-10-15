require('./scss/sm_link.scss')

// header 上的小链接
Vue.component('com-head-sm-link',{
    props:['head'],
    template:`<div class="small-link">
    <span class="item" v-for="action in head.options">
        <a :href="action.url" class="login-link" v-text="action.label"></a>
        <span class="space" v-if="action != head.options[head.options.length-1]">&nbsp;|&nbsp;</span>
    </span>

    </div>`
})