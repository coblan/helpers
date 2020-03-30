<template>
    <div class="com-top-swiper" :class="ctx.class">
        <van-swipe class="my-swipe" :autoplay="3000" indicator-color="white">
            <van-swipe-item v-for="item in ctx.items">
                <div class="img-container" :style="get_style(item.image_url)"></div>
                <!--<img :src="item.image_url" alt="">-->
            </van-swipe-item>
        </van-swipe>
    </div>
</template>
<script>
    export default {
        props:['ctx'],
        mounted(){
            if(this.ctx.css){
                ex.append_css(this.ctx.css)
            }
        },
        methods:{
            get_style(image_url){
                return {'background-image':'url('+image_url +')'}
            }
        }
    }
</script>

<style scoped lang="scss">
    .img-container{
        background-size: cover;
        background-position: center;
        width: 100vw;
        height: 5rem;
    }
    /*img{*/
        /*width: 100vw;*/
        /*height: auto;*/
    /*}*/
    .my-swipe .van-swipe-item {

        /*color: #fff;*/
        /*font-size: 20px;*/
        /*line-height: 150px;*/
        /*text-align: center;*/
        /*background-color: #39a9ed;*/
    }
</style>