<template>
    <div class="com-live-info">
        <div class="content">
            <div class="info">
                <span v-text="ctx.info"></span>
            </div>
            <div>
                <component :is="op.editor" v-for="op in ctx.ops" :head="op" @click="onclick(op)"></component>
            </div>
        </div>

    </div>
</template>
<script>
export default{
    props:['ctx'],
    basename:'live-info',
    methods:{
        onclick(op){
            ex.eval(op.action)
        }
    }

}
</script>
<style scoped lang="scss">

.com-live-info{
    height: var(--app-height);
    position: relative;
    .content{
        position: absolute;
        top:50%;
        left: .2rem;
        right: .2rem;
        transform: translateY(-50%);
    }
    .info{
        padding: 0 .3rem 2rem .3rem;
        text-align: center;
        font-size: .4rem;
    }
}

</style>