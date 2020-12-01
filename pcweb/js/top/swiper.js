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

