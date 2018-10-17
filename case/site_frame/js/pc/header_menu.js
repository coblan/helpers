require('./scss/header_menu.scss')

Vue.component('com-header-menu',{
    props:['menu','active'],
    template:`<div class="header-menu">
        <span class="menu-item" v-for="act in menu">
            <a :class="{'active':active==act.name}" href="jacascript::void(0)" @click="on_click(act.link)"  v-text="act.label"></a>
        </span>
    </div>`,
    methods:{
        on_click:function(url){
            if(this.$listeners && this.$listeners.jump){
                this.$emit('jump',url)
            }else{
                Vue.nextTick(function(){
                    location= url
                })
            }
        }
    }

})