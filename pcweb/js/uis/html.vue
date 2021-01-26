<template>
    <div class="com-ui-html" :class="ctx.class" v-html="ctx.html"></div>
</template>
<script>
    export default {
        props:['ctx'],
        mounted(){
            if(this.ctx.css){
                ex.append_css(this.ctx.css)
            }
        }
    }
</script>