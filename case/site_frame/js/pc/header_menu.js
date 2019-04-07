require('./scss/header_menu.scss')

Vue.component('com-header-menu',{
    props:['menu','active'],
    template:`<div class="header-menu">
        <span class="menu-item" v-for="act in menu">
            <a :class="['clickable',{'active':active==act.name}]"  @click="on_click(act)"  v-text="act.label"></a>
        </span>
    </div>`,
    methods:{
        on_click:function(act){
            if(this.$listeners && this.$listeners.jump){
                this.$emit('jump',act)
            }else{
                location= act.link
            }
        }
    }

})