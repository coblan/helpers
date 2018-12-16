require('./scss/auto_more.scss')

Vue.component('com-auto-more',{
    props:['orgHeight'],
    data:function(){
        return {
            expanded:false
        }
    }, //onmousewheel="return false;"
    template:`<div class="com-auto-more" :style="{height:orgHeight}">
        <div class="outer-wrap" :style="{height:orgHeight}">
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
        var self=this
        setTimeout(function(){
            if( $(self.$el).find('.inn-wrap').height() > $(self.$el).height()+10){ // 10是为了去噪
                $(self.$el).addClass('has-overflow')

            }
        },100)

    },
    methods:{
        on_scroll:function(){
            return false
        },
        toggle:function(){
            if(this.expanded){
                $(this.$el).find('.outer-wrap').css('height',this.orgHeight )
                $(this.$el).removeClass('expanded')

            }else{
                $(this.$el).find('.outer-wrap').css( 'height',$(this.$el).find('.inn-wrap').height()+2 +'px' )
                $(this.$el).addClass('expanded')

            }
            this.expanded = !this.expanded

        }
    }
})