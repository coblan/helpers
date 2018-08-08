function init_table_ctx(ctx){
    ctx.search_args= ctx.search_args || {}

    ctx.row_sort =ctx.row_sort || {sortable:[]}
    ctx.footer =ctx.footer || []
    ctx.ops = ctx.ops || []
    ctx.row_pages= ctx.row_pages || {crt_page:1,total:0,perpage:20}

    ctx.row_filters=ctx.row_filters || []
    ctx.director_name =ctx.director_name || ''

    if(ctx.selectable == undefined){
        ctx.selectable =true
    }

    return ctx
}

function init_table_bus(bus){
    //bus.search_args= bus.search_args || {}
    //bus.row_sort =bus.row_sort || {sortable:[]}
    //bus.footer =bus.footer || []
    //bus.ops = bus.ops || []
    //bus.row_pages= bus.row_pages || {crt_page:1,total:0,perpage:20}

    bus = init_table_ctx(bus)
    bus.eventBus=new Vue()
    return bus
}


var ele_table={
    props:['bus'],
    created:function(){
        this.bus.table=this
    },
    data:function(){
        return {
            heads:this.bus.heads,
            //rows:this.bus.rows,
            search_args:this.bus.search_args,
            row_sort:this.bus.row_sort,
            footer:this.bus.footer
        }
    },
    mounted:function(){
        this.bus.eventBus.$on('search',this.bus_search)
        this.bus.eventBus.$on('pageindex-change',this.get_page)
        this.bus.eventBus.$on('operation',this.on_operation)
        this.bus.eventBus.$on('perpage-change',this.on_perpage_change)

    },
    methods:{
        bus_search:function(search_args){
            ex.assign(this.search_args,search_args)
            this.search()
        }
    },
    //watch:{
    //    bus_serarch_count:function(){
    //        this.search()
    //    }
    //},
    computed:{
        //bus_serarch_count:function(){
        //    return this.bus.search_count
        //},
        rows:{
            get:function(){
                return this.bus.rows
            },
            set:function(v){
                this.bus.rows=v
            }
        },
        //search_args:{
        //    get:function(){
        //        return this.bus.search_args
        //    },
        //    set:function(v){
        //        this.bus.search_args=v
        //    }
        //}
    },
    // height="100%"
    //style="width: 100%"
    mixins:[mix_table_data,mix_ele_table_adapter],
    template:`  <el-table class="table" ref="e_table"
                              :data="rows"
                              border
                              show-summary
                              :fit="false"
                              :stripe="true"
                              size="mini"
                              @sort-change="sortChange($event)"
                              @selection-change="handleSelectionChange"
                              :summary-method="getSum">
                        <el-table-column v-if="bus.selectable"
                                type="selection"
                                width="55">
                        </el-table-column>

                        <template  v-for="head in heads">

                            <el-table-column v-if="head.editor"
                                             :show-overflow-tooltip="is_show_tooltip(head) "
                                             :label="head.label"
                                             :prop="head.name.toString()"
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
`
}
var ele_operations={
    props:['bus'],
    //                      :disabled="get_attr(op.disabled)"
    //v-show="! get_attr(op.hide)"
    template:`<div class="oprations" style="padding: 5px;">
                <component v-for="op in ops"
                           :is="op.editor"
                           :ref="'op_'+op.name"
                           :head="op"
                           @operation="on_operation(op)"></component>
            </div>`,
    data:function(){
        return {
            ops:this.bus.ops,
        }
    },
    methods:{
        get_attr:function (attr){
            return this.bus.table.get_attr(attr)
        },
        on_operation:function(op){
            this.bus.eventBus.$emit('operation',op)
        }
    }
}

var ele_filter={
    props:['bus'],
    computed:{
    },
    template:` <com-filter class="flex" :heads="bus.row_filters" :search_args="bus.search_args"
                        @submit="search()"></com-filter>`,
    methods:{
        search:function(){
            this.bus.eventBus.$emit('search',this.bus.search_args)
        }
    }
}

var ele_page={
    props:['bus'],
    data:function(){
        return {
            row_pages:this.bus.row_pages,
            search_args:this.bus.search_args
        }
    },
    methods:{
        on_page_change:function(v){
            this.bus.eventBus.$emit('pageindex-change',v)
        },
        on_perpage_change:function(v){
            this.bus.eventBus.$emit('perpage-change',v)
        }
    },
    //  @size-change="on_perpage_change"
    //@current-change="get_page"
    template:` <el-pagination
                         @size-change="on_perpage_change"
                        @current-change="on_page_change"
                        :current-page="row_pages.crt_page"
                        :page-sizes="[20, 50, 100, 500]"
                        :page-size="row_pages.perpage"
                        layout="total, sizes, prev, pager, next, jumper"
                        :total="row_pages.total">
                </el-pagination>`
}

Vue.component('com-table-bus',ele_table)
Vue.component('com-table-bus-ops',ele_operations)
Vue.component('com-table-bus-filter',ele_filter)
Vue.component('com-table-bus-page',ele_page)

window.init_table_ctx=init_table_ctx
window.init_table_bus=init_table_bus
window.ele_table_logic=ele_table
window.ele_table_page_logic=ele_page