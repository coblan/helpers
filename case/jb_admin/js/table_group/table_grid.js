require('./scss/table_grid.scss')
var ele_table= {
    props: ['bus'],
    created: function () {
        //this.bus.table = this

    },
    data: function () {
        this.parStore=ex.vueParStore(this)
        return {
            heads: this.parStore.heads,
            //rows:this.parStore.rows,
            search_args: this.parStore.search_args,
            row_sort: this.parStore.row_sort,
            //selectable:this.parStore.selectable,

        }
    },
    mounted: function () {
        //this.bus.eventBus.$on('search', this.bus_search)
        //this.bus.eventBus.$on('pageindex-change', this.get_page)
        //this.bus.eventBus.$on('operation', this.on_operation)
        //this.bus.eventBus.$on('perpage-change', this.on_perpage_change)
        this.parStore.e_table = this.$refs.e_table
    },


    computed: {
        rows:function(){
            return this.parStore.rows
        },
        selected:function(){
            return this.parStore.selected
        },
        footer:function(){
            return this.parStore.footer
        }
        //bus_serarch_count:function(){
        //    return this.bus.search_count
        //},
        //rows: {
        //    get: function () {
        //        return this.bus.rows
        //    },
        //    set: function (v) {
        //        this.bus.rows = v
        //    }
        //},
        //footer: {
        //    get: function () {
        //        return this.bus.footer
        //    },
        //    set: function (v) {
        //        this.bus.footer = v
        //    }
        //}
        //search_args:{
        //    get:function(){
        //        return this.bus.search_args
        //    },
        //    set:function(v){
        //        this.bus.search_args=v
        //    }
        //}
    },
    watch:{
        selected:function(newvalue,old){
            if(newvalue.length==0 && old.length !=0){
                this.$refs.e_table.clearSelection()
            }
        }
    },
    // height="100%"
    //style="width: 100%"
    mixins: [mix_table_data, mix_ele_table_adapter],
    template: `  <div style="position: absolute;top:0;left:0;bottom: 0;right:0;">
        <el-table class="table flat-head" ref="e_table"
                              :data="rows"
                              border
                              show-summary
                              :span-method="parStore.arraySpanMethod"
                              :row-class-name="tableRowClassName"
                              :fit="false"
                              :stripe="true"
                              size="mini"
                              height="100%"
                              style="width: 100%"
                              @sort-change="parStore.sortChange($event)"
                              @selection-change="parStore.handleSelectionChange"
                              :summary-method="getSum">
                        <el-table-column v-if="parStore.selectable"
                                type="selection"
                                width="55">
                        </el-table-column>

                        <template  v-for="head in parStore.heads">

                            <el-table-column v-if="head.editor"
                                             :show-overflow-tooltip="parStore.is_show_tooltip(head) "
                                             :label="head.label"
                                             :prop="head.name.toString()"
                                             :sortable="parStore.is_sort(head)"
                                             :width="head.width">
                                <template slot-scope="scope">
                                    <component :is="head.editor"
                                               @on-custom-comp="on_td_event($event)"
                                               :row-data="scope.row" :field="head.name" :index="scope.$index">
                                    </component>

                                </template>

                            </el-table-column>

                            <el-table-column v-else
                                             :show-overflow-tooltip="parStore.is_show_tooltip(head) "
                                             :prop="head.name.toString()"
                                             :label="head.label"
                                             :sortable="parStore.is_sort(head)"
                                             :width="head.width">
                            </el-table-column>

                        </template>

                    </el-table>
                    </div>
`,
    methods: {
        tableRowClassName:function({row, rowIndex}){
            return row._css_class
        },
        bus_search: function (search_args) {
            ex.assign(this.search_args, search_args)
            this.search()
        },
        on_td_event:function(e){
            var fun_name = e.fun || e.name // 以后都用fun
            if(e.head && e.head.arg_filter){
                var filter_fun=arg_filter[e.head.arg_filter]
                var normed_args = filter_fun(e.row,e.head)
                this.parStore[fun_name](normed_args)
            }else{
                this.parStore[fun_name](e)
            }
        }
    },
    //watch:{
    //    bus_serarch_count:function(){
    //        this.search()
    //    }
    //},
}
Vue.component('com-table-grid',ele_table)

var arg_filter={
    field:function(row,head){
        return row[head.field]
    }
}

