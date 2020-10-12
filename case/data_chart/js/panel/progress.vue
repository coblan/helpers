<template>
<div class="month-progress">
    <b v-text="ctx.label"></b>
    <div class="mypannel">
        <table class="mytable">
            <tr class="item" v-for="item in ctx.items">
                <td class="" v-text="item.label"></td>
                <td >
                    <div class="mybar">
                        <el-progress :color="customColorMethod" :text-inside="true" :stroke-width="20" :percentage="item.percent" status="exception"></el-progress>
                    </div>
                </td>
                <td>
                    <span v-text="item.text"></span>
                </td>

            </tr>
        </table>

    </div>


</div>
</template>
<script>
    export default {
        props:['ctx'],
        data(){
            return {
            }
        },
        methods:{
            customColorMethod(percentage) {
                if (percentage < 30) {
                    return '#909399';
                } else if (percentage < 70) {
                    return '#e6a23c';
                } else {
                    return '#67c23a';
                }
            },
        }
    }
</script>

<style scoped lang="scss">
    .mypannel{
        background-color: white;
        padding: 20px;
        margin: 10px 0;
    }
    .mytable{
        td{
            padding: 20px;
        }
    }
    .mybar{
        width: 300px;
    }
</style>