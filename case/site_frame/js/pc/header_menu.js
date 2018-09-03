require('./scss/header_menu.scss')

Vue.component('com-header-menu',{
    props:['menu','active'],
    template:`<div class="header-menu">
        <span class="menu-item" v-for="act in menu">
            <a :class="{'active':active==act.name}"  :href="act.link" v-text="act.label"></a>
        </span>
    </div>`,

})