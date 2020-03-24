require('./styl/swiper.styl')
Vue.component('com-top-swiper',{
    props:['ctx'],
    template:`<div class="com-top-swiper">
    <div class = 'web-wrap content'>
        <el-carousel :interval="5000" arrow="always">
            <el-carousel-item v-for="item in ctx.items" :key="item.name">
            <component :is="item.editor" :ctx="item"></component>
            </el-carousel-item>
      </el-carousel>
    </div>

    </div>`
})

Vue.component('com-swiper-image',{
    props:['ctx'],
    template:`<div class="com-swiper-image" :style="mystyle">
    <div class="mylabel" v-if="ctx.label" v-text="ctx.label"></div>
    </div>`,
    computed:{
        mystyle(){
            return {
                'background-image':'url('+this.ctx.image_url+')'
            }
        }
    }
})