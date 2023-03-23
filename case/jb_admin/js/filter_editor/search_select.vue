<template>
    <div class="com-filter-search-select">
        <el_select :row="search_args" :head="head"></el_select>
    </div>
</template>

<script>
    import el_select from '../field_editor/select.vue'
    export default {
        props: ['head', 'search_args'],
        components:{
            el_select
        },
        data(){
            this.head.filterable = true
            this.head.placeholder = this.head.label
            this.head.no_wrap=true
            return {
            }
        }
    }
</script>