<template>
    <div class="com-layout-div" :class="ctx.class">
        <component class="myitem" v-for="item in ctx.items" :is="item.editor" :key="item.name" :ctx="item"></component>
    </div>
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