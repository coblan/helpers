require('./styl/caption2.styl')

Vue.component('com-ti-caption2',{
    props:['ctx'],
    template:`<div class="com-ti-caption2" :class="ctx.class">
    <div class="image-content"  @mouseover="on_enter" @mouseout="on_leave">
        <div class="image-panel" :style="mystyle"></div>
    </div>

    <div class="text-content">
        <div class="title" v-text="ctx.title"></div>
        <div class="sub-title" v-text="ctx.sub_title"></div>
    </div>

    </div>`,
    computed:{
        mystyle(){
            return {
                'background-image':'url('+this.ctx.image_url+')'
            }
        }
    },
    methods:{
        on_enter(){
            $(this.$el).find('.image-panel').velocity('stop')
                .velocity({
                scaleX:1.1,
                scaleY:1.1,
            },{
                duration:2000,
                delay:200,
            });
        },
        on_leave(){
            $(this.$el).find('.image-panel').velocity('stop')
                .velocity({
                scaleX:1,
                scaleY:1,
            },{
                duration:1000,
            }  );
        }
    }

})