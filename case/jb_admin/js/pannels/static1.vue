<template>
    <div class="com-pan-static1">
        <b v-text="ctx.label">基本统计</b>
        <div class="my-panel">
            <div class="today-item" v-for="row in ctx.rows" :class="[ctx.class,{clickable:row.action}]" @click="onclick(row)">
                <span v-text="row.value"></span><br>
                <span v-text="row.label"></span>
            </div>
        </div>

    </div>
</template>
<script>
    export default {
        props:['ctx'],
        methods:{
            onclick(row){
                if(row.action){
                    ex.eval(row.action,{head:row})
                }
            }
        }
    }
</script>

<style scoped lang="scss">
    .my-panel{
        background-color: white;
        padding: 0 2rem;
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    .today-item{
        display: inline-block;
        margin: 2rem;
        width: 20rem;
        padding-bottom: 1rem;
        text-align: center;
        border-bottom: 1px solid #dadada;
    }
</style>