var ele_filter={
    data:function(){
        this.parStore=ex.vueParStore(this)
        return {
            row_filters:this.parStore.row_filters,
            search_args:this.parStore.search_args
        }
    },
    template:` <com-filter class="flex" :heads="row_filters" :search_args="search_args"
                        @submit="search()"></com-filter>`,
    methods:{
        search:function(){
            this.parStore.search()
            //this.bus.eventBus.$emit('search',this.bus.search_args)
        }
    }
}

Vue.component('com-table-filters',ele_filter)