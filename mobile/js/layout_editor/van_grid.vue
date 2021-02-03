<template>
    <div class="com-van-grid">
        <div class="mytitle" v-text="ctx.title"></div>
        <van-grid square class="myvant-grid">
            <van-grid-item
                    v-for="head in ctx.heads"
                    :text="head.label"
                    @click="on_click(head)"
            >
                <template #icon>
                    <van-image :src="head.icon" />
                </template>
            </van-grid-item>
        </van-grid>

    </div>

</template>

<script>
    export default {
        props:['ctx'],
        methods:{
            on_click(head){
                var click_express = head.click_express || head.action
                if(click_express){
                    ex.eval(click_express,{head:head})
                }
            }
        }
    }
</script>
<style lang="scss">
.com-van-grid{
    margin: .3rem 0;
    .mytitle{
        font-size: .3rem;
        font-weight: 400;
        color: #636363;
        margin: .2rem;
    }
    .myvant-grid{
        background-color:white;
    }
    .van-image img{
        height: .7rem;
        width: auto;
    }
    .van-grid-item__icon-wrapper{
        margin-bottom: .2rem;
    }
}
</style>