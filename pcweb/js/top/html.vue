<template>
    <div class="com-top-html" :class="ctx.class">
        <div class="web-wrap" v-html="ctx.html"></div>
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
<style lang="scss">
.com-top-html{

    img{
        max-width: 100%;
    }
}
</style>