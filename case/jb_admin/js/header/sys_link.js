require('./styl/sys_link.styl')

Vue.component('com-head-sys-link',{
    props:['head'],
    template:`<div :class="['com-head-sys-link',{active:head.active}]" @click="on_click()">
    <span v-text="head.label"></span>
    </div>`,
    methods:{
        on_click:function(){
            if(this.head.link){
                location = link
            }
        }
    }
})