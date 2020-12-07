<template>
    <div class="com-layout-div" :class="ctx.class">
        <b v-if="ctx.label" v-text="ctx.label"></b>
        <div class="div-wrap">
            <component class="div-item" v-for="item in ctx.items" :is="item.editor" :key="item.name" :ctx="item"></component>
        </div>
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