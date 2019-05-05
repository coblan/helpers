require('./styl/sys_link.styl')

Vue.component('com-headbar-sys-link',{
    props:['head'],
    template:`<li :class="['com-headbar-sys-link user-menu',{active:head.active,link:head.link}]" @click="on_click()">
    <span v-text="head.label"></span>
    </li>`,
    methods:{
        on_click:function(){
            if(this.head.link){
                location = this.head.link
            }
        }
    }
})