require('./styl/caption.styl')
/*
* | 图片 |
* |------|
* |描述  |
*
* hover时，边框变化，每行4个
* */
Vue.component('com-ti-caption',{
    props:['ctx'],
    template:`<div class="com-ti-caption" :class="ctx.class">
    <div class="image-content" :style="mystyle" ></div>
    <div class="text-content">
        <div class="title" v-text="ctx.title"></div>
        <div class="sub-title" v-text="ctx.sub_title"></div>
    </div>
    </div>`,
    mounted(){
        if(this.ctx.css){
            ex.append_css(this.ctx.css)
        }
    },
    computed:{
        mystyle(){
            return {
                'background-image':'url('+this.ctx.image_url+')'
            }
        }
    }

})