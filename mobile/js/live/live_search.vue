<template>
    <div class="com-live-search">
        <van-search v-model="value" placeholder="请输入搜索关键词"  show-action>
            <template v-slot:action>
                <div  @click="onSearch">搜索</div>
            </template>
        </van-search>
    </div>
</template>
<script>
    export default {
        props:['ctx'],
        basename:'live-search',
        data(){
            return {
                value:''
            }
        },
        methods:{
            onSearch(){

            }
        }
    }
</script>
<style lang="scss" scoped>
.com-live-search{
    background-color: white;
}
</style>