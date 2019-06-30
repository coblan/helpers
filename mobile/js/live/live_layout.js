require('./styl/live_fields.styl')

var live_layout = {
    props:['ctx'],
    basename:'live-layout',
    template:`<div class="com-live-layout">
        <!--<com-uis-nav-bar :title="ctx.title" :back="can_back" ></com-uis-nav-bar>-->
        <component :is="head.editor" v-for="head in ctx.layout_editors" :ctx="head"></component>
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
    deactivated(){
        this.scroll = $(this.$el).find('.com-fileds-panel').scrollTop()
    },
    activated() {
        if( this.scroll){
            var count =0
            var index =  setInterval(()=>{
                $(this.$el).find('.com-fileds-panel').scrollTop( this.scroll)
                count+=30
                if(count > 160){
                    clearInterval(index)
                }
            },30)
        }
    },
    //methods:{
    //    onAfterEnter(){
    //        if( this.scroll){
    //            $(window).scrollTop( this.scroll)
    //        }
    //    }
    //}

}



window.live_layout = live_layout