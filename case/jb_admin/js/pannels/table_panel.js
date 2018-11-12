var table_panel={
    props:['ctx'],
    data:function(){
        return {
            par_row:this.ctx.par_row,
            heads:this.ctx.heads,
            selectable:this.ctx.selectable,

            row_filters:this.ctx.row_filters,
            row_sort:this.ctx.row_sort,
            director_name:this.ctx.director_name,
            row_pages:{},
            rows:[],
            footer:[],
            selected:[],
            del_info:[],
            search_args: this.ctx.search_args || {},

            height:350,
        }
    },
    mixins:  [mix_table_data,mix_ele_table_adapter],

    template:`<div class="com-table-panel" style="height: 100%;padding-left: 10px">

            <div class="rows-block flex-v" style="height: 100%">
                <div class='flex' style="min-height: 3em;" v-if="row_filters.length > 0">
                    <com-filter class="flex" :heads="row_filters" :search_args="search_args"
                                @submit="search()"></com-filter>
                    <div class="flex-grow"></div>
                </div>
                <div class="box box-success flex-grow flex-v" >
                    <div class="table-wraper flex-grow" style="position: relative">
                    <div style="position: absolute;top:0;right:0;left:0;bottom: 0">
                     <el-table class="table" ref="e_table"
                                      :data="rows"
                                      border
                                      show-summary
                                      :fit="false"
                                      :stripe="true"
                                      size="mini"
                                      @sort-change="sortChange($event)"
                                      @selection-change="handleSelectionChange"
                                      :summary-method="getSum"
                                      height="100%"
                                      style="width: 100%">
                                <el-table-column
                                        v-if="selectable"
                                        type="selection"
                                        width="55">
                                </el-table-column>

                                <template  v-for="head in heads">

                                    <el-table-column v-if="head.editor"
                                                     :show-overflow-tooltip="is_show_tooltip(head) "
                                                     :label="head.label"
                                                     :sortable="is_sort(head)"
                                                     :width="head.width">
                                        <template slot-scope="scope">
                                            <component :is="head.editor"
                                                       @on-custom-comp="on_td_event($event)"
                                                       :row-data="scope.row" :field="head.name" :index="scope.$index">
                                            </component>

                                        </template>

                                    </el-table-column>

                                    <el-table-column v-else
                                                     :show-overflow-tooltip="is_show_tooltip(head) "
                                                     :prop="head.name.toString()"
                                                     :label="head.label"
                                                     :sortable="is_sort(head)"
                                                     :width="head.width">
                                    </el-table-column>

                                </template>

                            </el-table>
                     </div>

                    </div>
                    <div style="margin-top: 10px;">
                         <el-pagination
                                @size-change="on_perpage_change"
                                @current-change="get_page"
                                :current-page="row_pages.crt_page"
                                :page-sizes="[20, 50, 100, 500]"
                                :page-size="row_pages.perpage"
                                layout="total, sizes, prev, pager, next, jumper"
                                :total="row_pages.total">
                        </el-pagination>
                    </div>
                </div>
        </div>
    </div>`
}

window.com_table_panel=table_panel
Vue.component('com-table-panel',table_panel)