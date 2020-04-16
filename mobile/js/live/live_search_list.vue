<template>
    <div class="com-live-search-list">
        <van-search v-model="value" placeholder="请输入搜索关键词"
                    show-action>
            <template v-slot:left>
                <div style="width: .4rem" @click="on_back_action">
                    <van-icon name="arrow-left" />
                </div>

            </template>
            <template v-slot:action>
                <div  @click="onSearch">搜索</div>
            </template>
        </van-search>

        <van-list
                v-model="loading"
                :finished="finished"
                finished-text="没有更多了"
                :immediate-check="false"
                @load="onLoad"
                :class="ctx.content_class"
                @touchmove.stop
        >
            <van-pull-refresh  v-model="freshing" @refresh="onRefresh">
                <component class="content-wrap" :is="table_editor" :ctx="{rows:childStore.rows}"  @select="triggerBlockClick($event)"></component>
            </van-pull-refresh>
        </van-list>

        <div v-if="ctx.footer" class="footer-content">
            <component :is="ctx.footer.editor"  :ctx="ctx.footer"></component>
        </div>


    </div>
</template>
<script>
    import {live_list} from './live_list'
    export default {
        props:['ctx'],
        basename:'live-search-list',
        data(){
            return {
                value:''
            }
        },
        mixins:[live_list],
        methods:{
            init(){
                if(this.ctx.css){
                    ex.append_css(this.ctx.css)
                }
                if(this.ctx.init_express){
                    ex.eval(this.ctx.init_express,{self:this,cs:this.childStore})
                }
            },
            onSearch(){
                this.childStore.search_args._q = this.value
                this.childStore.search().then((new_rows)=>{
                    this.childStore.$emit('finish-search',new_rows)
                })
            },
            on_back_action(){
                history.back()
            }
        }
    }
</script>
<style lang="scss" scoped>
    .com-live-search-list{
    }
</style>