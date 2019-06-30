require('./styl/live_fields.styl')

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



window.live_fields = live_fields