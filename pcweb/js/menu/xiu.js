require('./styl/xiu.styl')

Vue.component('com-xiu-menu',{
    template:`<div class="com-xiu-menu">
    <div class="web-wrap">
        <div class="brand" v-html="parStore.vc.head_bar_data.brand"></div>
        <div class="menu">
            <div class="action"  v-for="action in parStore.vc.menu">
                <a :class="{'active':is_active(action)}" :href="action.url" v-text="action.label"></a>
            </div>
        </div>
    </div>

    </div>`,
    data(){
        return {
            parStore:ex.vueParStore(this)
        }
    },
    methods:{
        is_active:function(action){
            if (action.url == location.pathname){
                return true
            }else{
                return false
            }
        },
    }
})