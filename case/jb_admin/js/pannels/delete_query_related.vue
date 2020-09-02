<template>
    <div class="com-delte-query-message">

        <div class="middle">
            <el-alert
                    title="以下关联选项会一起被删除，请确认!"
                    :closable="false"
                    type="warning">
            </el-alert>

            <el-tree
                    default-expand-all
                    :data="ctx.msg_list"
                    :props="defaultProps">
            </el-tree>
        </div>


        <div class="btn-pannel">
            <el-button size="mini" @click="on_cancel">取消</el-button>
            <el-button size="mini" type="danger" @click="on_click">确定删除</el-button>
        </div>

    </div>
</template>
<script>
    export default {
        props:['ctx'],
        data(){
            return {
                defaultProps:{
                    children: 'related',
                    label: 'str'
                }
            }
        },
        methods:{
            on_cancel(){
                this.$emit('finish')
            },
            on_click(){
                this.ctx.genStore.delete_selected()
                this.$emit('finish')
            }
        }
    }
</script>

<style scoped lang="scss">
.com-delte-query-message{
    display: flex;
    flex-direction: column;
    height: 100%;
}
.middle{
    flex-grow: 10;
    overflow: auto;
}
.btn-pannel{
    border-top:1px solid #dddddd;
    text-align: right;
    padding: 5px 20px;
}
</style>