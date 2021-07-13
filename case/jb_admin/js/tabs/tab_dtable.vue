<template>
    <div class="com-tab-table flex-v" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 1em;">
        <director_table
                :filter-heads='head.row_filters'
                :table-rows="rows"
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
                :extend-logic="extend_logic"
        ></director_table>
    </div>
</template>

<script>
    import  director_table,{DTableLogic} from  '../pannels/director_table.vue'
    const { ref, reactive,computed ,onMounted,getCurrentInstance } = VueCompositionAPI

    class TabDTableLogic extends DTableLogic{
        getSetup(props){
            return {
                par_row:props.par_row
            }
        }
    }

    export default {
        props:['tab_head','par_row'],
        components:{
            director_table,
        },
        setup(porps){
//            var dtable = ref(null)
//            onMounted(()=>{
//                debugger
//                console.log(dtable.value)
//            })

            return {
//                dtable:dtable,
                extend_logic:TabDTableLogic,
//                extend_logic:{
//                    par_row:porps.par_row
//                }
            }
        },
        data(){
            var heads_ctx = this.tab_head.table_ctx
            heads_ctx.search_args= heads_ctx.search_args || {}
            var rows= ex.copy( heads_ctx.rows )
            return {
                head:heads_ctx,
                rows:rows,
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