require('./scss/kuaifawu_menu.scss')

Vue.component('com-kuaifawu-menu',{
    props:['label','menu'],
    data:function(){
        return {
            expand:false,
            active_act:{}
        }
    }, //
    template:`<div class="kuaifawu-menu" @mouseenter="expand=true" @mouseleave="on_mouseleave()">
        <!--<span class="menu-item" v-for="act in menu">-->
            <!--<a :class="{'active':active==act.name}"  :href="act.link" v-text="act.label"></a>-->
        <!--</span>-->

            <span v-text="label" class="menu-button"></span>

            <div v-show="expand" class="actions">
                <com-kuaifawu-menu-item v-for="act in menu" :act="act"
                    :class="['menu-item',{'active':active_act.name==act.name}]" @mouseenter.native="active_act=act"></com-kuaifawu-menu-item>
            </div>
            <com-kuaifawu-menu-links class="menu-links" v-show="active_act.name" :act="active_act"></com-kuaifawu-menu-links>

    </div>`,
    methods:{
        on_mouseleave:function(){
            this.expand=false
            this.active_act={}
        }
    }

})

Vue.component('com-kuaifawu-menu-item',{
    props:['act'],
    template:`<div>
        <span v-text="act.label"></span>
    </div>`
})

Vue.component('com-kuaifawu-menu-links',{
    props:['act'],
    template:`<div>
        <span v-text="act.label"></span>
    </div>`
})