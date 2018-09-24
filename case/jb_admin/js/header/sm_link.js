//require('./scss/dropdown.scss')


Vue.component('com-head-sm-link',{
    props:['head'],
    template:`<div>
    <span v-for="action in head.options">
        <a :href="action.url" class="login-link" v-text="action.label"></a>
        <span v-if="action != head.options[head.options.length-1]">&nbsp;|&nbsp;</span>
    </span>

        <!--<a href="/accounts/regist">注册</a>-->

    </div>`
})