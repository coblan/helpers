var ele_page={

    data:function(){
        var parStore = ex.vueParStore(this)
        this.parStore= parStore.table?parStore.table:parStore
        return {
            row_pages:this.parStore.row_pages,
            search_args:this.parStore.search_args
        }
    },
    methods:{
        on_page_change:function(v){
            this.search_args._page=v
            this.parStore.getRows()
            //this.bus.eventBus.$emit('pageindex-change',v)
        },
        on_perpage_change:function(v){
            this.search_args._perpage=v
            this.parStore.search()
            //this.bus.eventBus.$emit('perpage-change',v)
        }
    },
    //  @size-change="on_perpage_change"
    //@current-change="get_page"
    template:` <el-pagination
                         @size-change="on_perpage_change"
                        @current-change="on_page_change"
                        :current-page="row_pages.crt_page"
                        :page-sizes="row_pages.options ||  [20, 50, 100]"
                        :page-size="row_pages.perpage"
                        layout="total, sizes, prev, pager, next, jumper"
                        :total="row_pages.total">
                </el-pagination>`
}

Vue.component('com-table-pagination',ele_page)