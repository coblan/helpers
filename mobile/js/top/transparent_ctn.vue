<template>
    <div class="com-top-transparent-ctn" :style="mystyle">
        <div class = 'web-wrap'>
            <div v-if="ctx.title" class="title" v-text="ctx.title"> </div>
            <div v-if="ctx.subtitle" class="subtitle" v-text="ctx.subtitle"></div>
            <div class="block-content">
                <component v-for="item in ctx.items" :is="item.editor" :ctx="item"></component>
            </div>
        </div>
    </div>
</template>
<script>
    export default {
        props:['ctx'],
        computed:{
            mystyle(){
                return {'background-image':'url('+ this.ctx.image_url +')'}
            }
        }
    }
</script>

<style scoped lang="scss">
    .com-top-transparent-ctn{
        height:5rem;
        width: 100%;
        position:relative;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;

    .web-wrap{
        position: absolute;
        top:50%;
        left: 50%;
        transform: translate(-50%,-50%);
        width: 100%;
    }
        .title{
            color:white;
            letter-spacing:.1rem;
            text-align:center;
            font-size:.4rem;
            line-height:1rem;
        }
    .subtitle{
        color: #eeeeee;
        /*letter-spacing: .1rem;*/
        text-align: center;
        font-size:.3rem;
        line-height: .4rem;
    }


}





</style>