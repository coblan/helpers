require('./styl/sys_link.styl')

Vue.component('com-headbar-space',{
    props:['head'],
    template:`<li :class="['com-headbar-space',head.class]" :style="head.style">
    </li>`,
})