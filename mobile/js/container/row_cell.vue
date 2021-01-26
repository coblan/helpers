<template>
    <div class="com-list-row-cell">
        <van-cell  v-for="row in rows" title="单元格" :is-link="has_nextlevel" clickable @click="on_click(row)">
            <template slot="title">
                <div class="material-wave content"  >
                    <component :is="head.editor" v-for="head in heads"
                               :class="head.class" :head="head" :row="row"></component>
                </div>
            </template>
        </van-cell>
        <div class="no-data" v-if="rows.length == 0">暂无数据</div>
    </div>
</template>
<script>
export default {
    props:['heads','rows'],
    data(){
        var parStore = ex.vueParStore(this)
        return {
            parStore:parStore
        }
    },
    mounted(){
        if(this.option && this.option.style){
            ex.append_css(this.option.style)
        }
    },
    computed:{
        has_nextlevel(){
            if(this.parStore.vc.ctx.block_click){
                return true
            }else{
                return false
            }
        }
    },
    methods:{
        on_click(row){
            ex.eval(this.parStore.vc.ctx.block_click,{ps:this.parStore,row:row})
        }
    }
}

</script>

<style scoped lang="scss">
    .com-list-row-cell{
        overflow: auto;
        min-height: calc(var(--app-height) - 80px );
    }
.content{
    display: flex;
    width: 90%;
    overflow: hidden;
}
    .no-data{
        position: absolute;
        top:30%;
        left: 50%;
        transform: translateX(-50%);
    }
    .loading .no-data{
        display: none;
    }
</style>