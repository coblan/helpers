<template>
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
            <component class="content-wrap" :is="table_editor" :heads="ctx.heads" :rows="childStore.rows"  @select="triggerBlockClick($event)"></component>
        </van-pull-refresh>
    </van-list>
</template>
<script>
    import {get_table_store} from '../store/table_store.js'
    var table_store = get_table_store()
    table_store.name= 'dog'
    table_store.methods.getRows =function(){
            // 相比原来的接口，这里只是去掉cfg.show_load()
            var post_data=[{fun:'get_rows',director_name:this.director_name,search_args:this.search_args}]
            return ex.post('/d/ajax',JSON.stringify(post_data)).then(resp=> {
                this.rows = this.filter_load_row( resp.get_rows.rows )
            this.parents = resp.get_rows.parents
            ex.vueAssign( this.row_pages,resp.get_rows.row_pages)
            return this.rows
        })
    }
    export default {
        props:['ctx','passive'],
        data(){
            var childStore = new Vue(table_store)
            childStore.rows= this.ctx. rows || []
            childStore.vc = this
            childStore.director_name = this.ctx.director_name
            if(this.ctx.search_args){
                ex.vueAssign(childStore.search_args,this.ctx.search_args)
            }
            if(this.ctx.filter_express){
                let env = ex.eval(this.ctx.filter_express,{ps:this})
                ex.vueAssign(childStore.search_args, env)
            }

            return {
                freshing:false,
                loading:false,
                finished:false,
                childStore:childStore,
                table_editor: this.ctx.table_editor || 'com-ctn-table-van-cell',
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
            if(!this.passive){
                this.init()
            }
        },
        computed:{
            is_page(){
                if(this.ctx.is_page ==undefined){
                    return true
                }else{
                    return this.ctx.is_page
                }

            },
            can_back(){
                return this.$root.stack.length >1
            }
        },
        methods:{
            init(){
                if(this.ctx.css){
                    ex.append_css(this.ctx.css)
                }
                if(this.ctx.init_express){
                    ex.eval(this.ctx.init_express,{self:this,cs:this.childStore})
                }else  if(!this.ctx.rows || this.ctx.rows.length==0){
                    this.childStore.search()
                }
            },
            onRefresh(){
                console.log('刷新')
                this.childStore.search().then(()=>{
                    this.freshing = false
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
        },
    }
</script>
<style scoped>

</style>