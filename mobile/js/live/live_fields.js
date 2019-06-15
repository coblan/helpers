var live_fields={
    props:['ctx'],
    basename:'live-fields',
    template:`<div class="com-live-fields">
        <com-uis-nav-bar :title="ctx.title" :back="can_back" ></com-uis-nav-bar>
        <com-fields-panel :ctx="ctx"></com-fields-panel>
    </div>`,
    data(){
        var childStore = new Vue()
        childStore.vc=this
        return {
            childStore:childStore
        }
    },
    computed:{
        can_back(){
            return this.$root.stack.length >1
        }
    },
}



window.live_fields = live_fields