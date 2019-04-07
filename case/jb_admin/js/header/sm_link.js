require('./scss/sm_link.scss')

// header 上的小链接,例如右上角的  [登录 | 注册  ]
Vue.component('com-head-sm-link',{
    props:['head'],
    template:`<div class="small-link">
    <span class="item" v-for="action in head.options">
        <a  @click="on_click(action)" class="login-link clickable" v-text="action.label"></a>
        <span class="space" v-if="action != head.options[head.options.length-1]">&nbsp;|&nbsp;</span>
    </span>
    </div>`,
    methods:{
        on_click:function(action){
            if(this.$listeners && this.$listeners.jump){
                this.$emit('jump',action)
            }else{
                location = action.link
            }
        }
    }
})