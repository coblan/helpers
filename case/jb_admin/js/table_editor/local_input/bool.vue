<template>
    <div class="com-table-local-bool" >
        <el-checkbox  v-model="rowData[field]"></el-checkbox>
    </div>
</template>
<script>
    export default {
        props:['rowData','field','index'],
        data(){
            return {

            }
        },
        methods:{

        }
    }
</script>
<style scoped lang="scss">
</style>