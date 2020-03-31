<template>
    <div class="com-top-caption" :class="ctx.class">
        <div v-if="ctx.location !='right'" class="img-container" :style="image_bg">

        </div>
        <!--<img v-if="ctx.location !='right'" :src="ctx.image_url" alt="">-->
        <div class="content">
            <div class="mytitle" v-if="ctx.title" v-text="ctx.title"></div>
            <div class="sub-title">
                <span v-text="ctx.sub_title"></span>
            </div>
        </div>
        <div v-if="ctx.location=='right'" class="img-container" :style="image_bg">

        </div>
        <!--<img v-if="ctx.location=='right'" :src="ctx.image_url" alt="">-->
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
        computed:{
            image_bg(){
                return {
                    'background-image':'url('+this.ctx.image_url +')'
                }
            }
        }
    }
</script>
<style scoped lang="scss">
.com-top-caption  {
   display: flex;
}
.img-container{
    width: 40vw;
    margin: .2rem;
    height: 40vw;
    background-size: cover;
    background-position: center;
}
.content{
    width: 50vw;
    padding: .2rem;
    line-height: .5rem;
    color: #5a5a5a;
}
.mytitle{
    border-bottom: 1px solid #c8c8c8;
    font-size: .3rem;
    padding-bottom: .2rem;
    margin-bottom: .2rem;
}
.sub-title{
    font-size: .26rem;
}

</style>