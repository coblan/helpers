require('./scss/auto_more.scss')

Vue.component('com-auto-more',{
    data:function(){
        return {
            expanded:false
        }
    }, //onmousewheel="return false;"
    template:`<div class="com-auto-more" >
        <div class="outer-wrap">
            <div class="inn-wrap">
                <slot></slot>
            </div>
        </div>

        <div class="toggle-btn clickable" @click="toggle()">
            <span v-if="expanded">收起</span>
            <span v-else>更多</span>
        </div>
    </div>`,
    mounted:function(){
        if( $(this.$el).find('.inn-wrap').height() > $(this.$el).height()){
            $(this.$el).addClass('has-overflow')
        }
    },
    methods:{
        on_scroll:function(){
            return false
        },
        toggle:function(){
            if(this.expanded){
                $(this.$el).find('.outer-wrap').css('height','3rem' )
                $(this.$el).removeClass('expanded')

            }else{
                $(this.$el).find('.outer-wrap').css( 'height',$(this.$el).find('.inn-wrap').height()+20 +'px' )
                $(this.$el).addClass('expanded')

            }
            this.expanded = !this.expanded

        }
    }
})