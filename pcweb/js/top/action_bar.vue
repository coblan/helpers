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
/*.action-panel{*/
    /*display: flex;*/
    /*.action{*/
        /*margin: 0 10px;*/
        /*padding: 5px 10px;*/
        /*cursor: pointer;*/
        /*line-height: 40px;*/

        /*&.active{*/
            /*border-bottom:  1px solid grey;*/
         /*}*/
    /*}*/
/*}*/
.action-panel{
    box-sizing: border-box;
    height: 60px;
    /*width: 100%;*/
    padding: 15px;
}
.action{
    font-size: 15px;
    height: 30px;
    line-height: 30px;
    padding-left: 15px;
    padding-right: 15px;
    display: inline-block;
    margin-right: 10px;
    cursor: pointer;
    border-radius: 2px;
}
.action.active{
    color: #ffffff;
    background-color: #80bcff;
    cursor: default;
    padding-right: 5px;
    &:after{
         content: '';
         width: 0;
         height: 0;
         border-left: 5px solid transparent;
         border-right: 5px solid transparent;
         border-top: 5px solid #80bcff;
         position: relative;
         top: 30px;
         right: 50%;
     }
}

</style>