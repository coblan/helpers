Vue.component('com-item-span',{
    props:['head','row'],
    template:`<span class="com-item-span" v-text="row[head.name]"></span>`
})