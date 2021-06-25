<template>
    <director_table
            :filter-heads='ctx.row_filters'
            :table-rows="ctx.rows"
            :table-heads="ctx.heads"
            :row-sort="ctx.row_sort"
            :row-pages="ctx.row_pages"
            :advise-heads="ctx.advise_heads"
            :advise-heads-cookie-path="ctx.advise_heads_cookie_path"
            :director-name="ctx.director_name"
            :operation-heads="ctx.ops"
            :footer="ctx.footer"
            :parents="ctx.parents"
            :search-args="ctx.search_args"
            ref="dtable"
            :extend-logic="extendLogic"
    >

    </director_table>
</template>
<script>
    import  director_table from  './director_table.vue'
    const { ref, reactive,computed ,onMounted,getCurrentInstance } = VueCompositionAPI

    class BackendTable{
        extendSetup(){
            return {}
        }
        getSetup(props){
            this. dtable = ref(null)
            this.connect_dtable_event()
            return {
                dtable:this.dtable,
                extendLogic:this.extendSetup(),
            }
        }
        connect_dtable_event(){
            const vc = getCurrentInstance()
            onMounted(()=>{
                this.dtable.value.childStore.$on('finish',(data)=>{
                    vc.emit('finish',data)
                })
            })
        }

    }
    export default {
        components:{
            director_table,
        },
        props:['ctx','extendLogic'],
        setup(props){

            return new BackendTable().getSetup(props)
        }
    }
</script>