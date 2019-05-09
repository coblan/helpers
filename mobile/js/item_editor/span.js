Vue.component('com-table-span',{
    props:['head','row'],
    template:`<span class="com-item-span" v-text="row[head.name]"></span>`
})