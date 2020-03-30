<template>
    <div class="com-top-swiper">
        <van-swipe class="my-swipe" :autoplay="3000" indicator-color="white">
            <van-swipe-item v-for="item in ctx.items">
                <img :src="item.image_url" alt="">
            </van-swipe-item>
        </van-swipe>
    </div>
</template>
<script>
    export default {
        props:['ctx'],
    }
</script>

<style scoped lang="scss">
    .my-swipe .van-swipe-item {
        img{
            max-width: 100vw;
            height: auto;
        }
        /*color: #fff;*/
        /*font-size: 20px;*/
        /*line-height: 150px;*/
        /*text-align: center;*/
        /*background-color: #39a9ed;*/
    }
</style>