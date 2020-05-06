<template>
    <div>
        <div class="web-wrap action-panel">
            <div class="action" :class="{active:crt_action == act.label}" @click="on_click(act)" v-for="act in ctx.actions">
                <span v-text="act.label"></span>
            </div>
        </div>

    </div>
</template>
<script>
    export default {
        props:['ctx'],
        data(){
            return {
                crt_action: this.ctx.actions[0].label
            }
        },
        methods:{
            on_click(act){
                this.crt_action = act.label
                ex.eval(act.action)
            }
        }
    }
</script>

<style scoped lang="scss">
.action-panel{
    display: flex;
    .action{
        margin: 0 10px;
        padding: 5px 10px;
        cursor: pointer;
        line-height: 40px;

        &.active{
            border-bottom:  1px solid grey;
         }
    }
}
</style>