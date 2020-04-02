<template>
    <div class="com-top-swiper" :class="ctx.class">
        <van-swipe class="my-swipe" :autoplay="5000" indicator-color="white">
            <van-swipe-item v-for="item in ctx.items">
                <div class="img-container" :style="get_style(item.image_url)">
                    <div v-if="item.label" class="ab-h-center image-label" v-text="item.label"></div>
                </div>
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
        width: var( --app-width );
        height: 5rem;
    }
    .image-label{
        width: 100%;
        background-color: rgba(0,0,0,.2);
        color: white;
        font-size: .3rem;
        height: .5rem;
        line-height: .5rem;
        letter-spacing: .06rem;
        text-align: center;
        top: 0;
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