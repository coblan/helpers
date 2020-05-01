<template>
    <div class="com-top-image-top-pad" :class="ctx.class">
      <div v-if="ctx.full_width"  >
        <div class="head">
            <img :src="ctx.image_url" alt="">
        </div>
        <div class="content web-wrap">
            <component :is="ctx.inn_editor" :ctx="ctx.inn_ctx"></component>
        </div>
    </div>
        <div v-else class="web-wrap" >
            <div class="head">
                <img :src="ctx.image_url" alt="">
            </div>
            <div class="content">
                <component :is="ctx.inn_editor" :ctx="ctx.inn_ctx"></component>
            </div>
        </div>

    </div>
</template>
<script>
    export default   {
        props:['ctx'],
        mounted(){
            if(this.ctx.css){
                ex.append_css(this.ctx.css)
            }
        }
    }
</script>
<style lang="scss" scoped>
.head{
    position: relative;
    height: 300px;

    img{
        z-index:-1;
        position:absolute;
        width: 100%;
        height: auto;
    }
}
.content{
    -moz-box-shadow:0px 0px 17px #ABABAB; -webkit-box-shadow:0px 0px 17px #ABABAB; box-shadow:0px 0px 17px #ABABAB;
    border-radius: 10px;
    background-color: white;
    min-height: 500px;
    width: 80%;
    margin: auto;
    padding: 40px 20px 20px 20px;
}
</style>