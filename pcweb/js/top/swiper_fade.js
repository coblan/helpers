require('./styl/swiper_fade.styl')

var swiper_fade={
    props:['ctx'],
    template:`<div class="com-top-swiper-fade" >
    <div class="bg-image" :style="mystyle"></div>

    <div class = 'web-wrap'>
        <!--<el-carousel :interval="5000" arrow="always" effect="fade">-->
            <!--<el-carousel-item v-for="item in ctx.items" :key="item.name">-->
            <!--<component :is="item.editor" :ctx="item"></component>-->
            <!--</el-carousel-item>-->
      <!--</el-carousel>-->
      <div class="swiper-container">
            <div class="swiper-wrapper">
             <component class="swiper-slide" v-for="item in ctx.items" :key='item.name' :is="item.editor" :ctx="item"></component>
           </div>
           <!-- Add Pagination -->
            <div class="swiper-pagination swiper-pagination-white"></div>
            <!-- Add Arrows -->
            <div class="swiper-button-next swiper-button-white"></div>
            <div class="swiper-button-prev swiper-button-white"></div>
      </div>

    </div>
    </div>`,
    data(){
        return {
            activeIndex:0,
        }
    },
    mounted(){
        var self =this
        Vue.nextTick(()=>{
            var swiper = new Swiper($(this.$el).find('.swiper-container'), {
                spaceBetween: 30,
                effect: 'fade',
                loop: true,
                autoplay: {
                    delay: 5000,
                    disableOnInteraction: false,
                },

                pagination: {
                    el: $(this.$el).find('.swiper-pagination'),
                    clickable: true,
                },
                navigation: {
                    nextEl: $(this.$el).find('.swiper-button-next'),
                    prevEl: $(this.$el).find('.swiper-button-prev'),
                },
                on:{
                    transitionStart: function(){
                        self.activeIndex = ( this.activeIndex -1 ) % self.ctx.items.length
                    },
                    transitionEnd: function(){

                    },
                },
            });
        })
    },
    computed:{
        mystyle(){
            return {
                'background-image':'url('+this.ctx.items[this.activeIndex].image_url+')'
            }
        }
    }
}

Vue.component('com-top-swiper-fade',function(resolve,reject){
    ex.load_css(js_config.js_lib.swiper_css)
    ex.load_js(js_config.js_lib.swiper).then(()=>{
        resolve(swiper_fade)
    })
})