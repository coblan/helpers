<template>
    <div class="com-top-list" :class="ctx.class">
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
                <component  class="content-wrap" :is="table_editor" :heads="ctx.heads"
                            :class="{'loading':loading,}"
                            :rows="childStore.rows"  @select="triggerBlockClick($event)"></component>
                <!--<row_cell v-else  class="content-wrap"  :heads="ctx.heads" :rows="childStore.rows"  @select="triggerBlockClick($event)"></row_cell>-->
            </van-pull-refresh>
        </van-list>
    </div>
</template>
<script>
    import row_cell from '../container/row_cell.vue'
    export default {
        props:['ctx'],
        components:{
            row_cell
        },
        data(){
            var childStore = new Vue(table_store)
            childStore.rows= this.ctx. rows || []
            childStore.vc = this
            childStore.director_name = this.ctx.director_name
            if(this.ctx.search_args){
                ex.vueAssign(childStore.search_args,this.ctx.search_args)
            }

            return {
                freshing:false,
                loading:false,
                finished:false,
                childStore:childStore,
                table_editor: this.ctx.table_editor || 'row_cell',
                scrollOptions: {
                    /* lock x-direction when scrolling horizontally and  vertically at the same time */
                    directionLockThreshold: 0,
                    click:true,
                    pullDownRefresh:{
                        txt:'刷新成功!',
                    },
                    pullUpLoad:{
                        txt:{ more: '', noMore: '没有更多了!' }
                    },

                },
            }
        },
        mounted(){
            if(this.ctx.css){
                ex.append_css(this.ctx.css)
            }
            this.init()
        },
        methods:{
            init(){
                if(this.ctx.css){
                    ex.append_css(this.ctx.css)
                }
                if(this.ctx.init_express){
                    ex.eval(this.ctx.init_express,{self:this,cs:this.childStore})
                }else  if(!this.ctx.rows || this.ctx.rows.length==0){
                    this.loading=true
                    this.childStore.search().then(()=>{
                        this.loading= false
                    })

                }
            },
            onRefresh(){
                console.log('刷新')
                this.loading = true
                this.childStore.search().then(()=>{
                    this.freshing = false
                    this.loading = false
                    this.finished=false
            })

            },
            onLoad(){
                console.log('加载')
                this.childStore.addNextPage().then(()=>{
                    this.loading = false
                if(this.childStore.search_args._page * this.childStore.row_pages.perpage >=  this.childStore.row_pages.total   ){
                    this.finished=true
                }else{
                    this.finished=false
                }
            })
            },
            triggerBlockClick(row){
                if(this.ctx.block_click){
                    ex.eval(this.ctx.block_click,{row:row,ps:this.childStore})
                }
            },
            onPullingUp(){

                this.childStore.addNextPage().then((new_rows)=>{
                    this.$refs.scroll.forceUpdate()
                this.childStore.$emit('finish-search',new_rows)
            })
            },
            onPullingDown(){

                this.childStore.search().then((new_rows)=>{
                    this.$refs.scroll.forceUpdate()
                this.childStore.$emit('finish-search',new_rows)
            })
            },

        }
    }
</script>
<style lang="scss">
    .com-top-html{
        img{
            max-width: 100%;
            height: auto;
        }
    }
    .content-wrap{
        height: 100%;
        width: 100%;
    }
</style>