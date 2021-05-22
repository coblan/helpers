<template>
    <div class="com-tab-table flex-v" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 1em;">
        <director_table
                :filter-heads='head.row_filters'
                :table-rows="head.rows"
                :table-heads="head.heads"
                :row-sort="head.row_sort"
                :row-pages="head.row_pages"
                :advise-heads="head.advise_heads"
                :advise-heads-cookie-path="head.advise_heads_cookie_path"
                :director-name="head.director_name"
                :operation-heads="head.ops"
                :footer="head.footer"
                :parents="head.parents"
                :search-args="head.search_args"
                ref="dtable"
        ></director_table>
    </div>
</template>

<script>
    import  director_table from  '../pannels/director_table.vue'
    export default {
        props:['tab_head','par_row'],
        components:{
            director_table,
        },
        data(){
            var heads_ctx = this.tab_head.table_ctx
            heads_ctx.search_args= heads_ctx.search_args || {}
            return {
                head:heads_ctx,
                parStore:ex.vueParStore(this),
            }
        },
        mounted(){
            if(this.tab_head.autoload || this.tab_head.autoload == undefined ){
                Vue.nextTick(()=>{
                    this.search()
                })
            }
            if(this.tab_head.mounted_express){
                ex.eval(this.tab_head.mounted_express,{vc:this,ps:this.parStore})
            }
        },
        methods:{
            search(){
                if(this.tab_head.filter_express){
                    var pp = ex.eval(this.tab_head.filter_express,{vc:this,ps:this.parStore})
                    ex.vueAssign(this.head.search_args,pp)
                }
                this.$refs.dtable.search()
            }
        }

    }
</script>