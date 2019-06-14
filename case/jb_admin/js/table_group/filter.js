var ele_filter={
    data:function(){
        this.parStore=ex.vueParStore(this)
        return {
            row_filters:this.parStore.row_filters,
            search_args:this.parStore.search_args
        }
    },
    template:` <com-filter class="flex" :heads="normed_heads" :search_args="search_args"
                        @submit="search()"></com-filter>`,
    computed:{
        normed_heads(){
            var out_ls=[]
            ex.each(this.row_filters,(head)=>{
                if(head.show){
                    if(!ex.eval(head.show,{ps:this.parStore,head:head})){
                        return
                    }
                }
                out_ls.push(head)
            })
            return out_ls
        }
    },
    methods:{
        search:function(){
            this.parStore.search()
            //this.bus.eventBus.$emit('search',this.bus.search_args)
        }
    }
}

Vue.component('com-table-filters',ele_filter)