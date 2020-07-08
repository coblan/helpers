<template>
<div class="com-top-html" v-html="ctx.html">
</div>
</template>
<script>
export default {
    props:['ctx'],
    data(){
        return {
            parStore:ex.vueParStore(this)
        }
    },
    mounted(){
        if(this.ctx.css){
            ex.append_css(this.ctx.css)
        }
    },
    methods:{
    }
}
</script>
<style lang="scss">
.com-top-html{
    img{
        max-width: 100%;
        height: auto;
    }
}
</style>