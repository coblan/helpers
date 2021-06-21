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
    export default {
        components:{
            director_table,
        },
        props:['ctx','extendLogic']
    }
</script>