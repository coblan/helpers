var ele_table_bus_page = {
    mixins:[ele_table_page_logic],
    template:` <el-pagination
                         @size-change="on_perpage_change"
                        @current-change="on_page_change"
                        :current-page="row_pages.crt_page"
                        :page-sizes="[20, 50, 100, 500]"
                        :page-size="row_pages.perpage"
                        layout="total, sizes, prev, pager, next"
                        :total="row_pages.total">
                </el-pagination>`

}

//  覆盖掉pc端的 同名 vuejs 组件
Vue.component('com-table-bus-page',ele_table_bus_page)