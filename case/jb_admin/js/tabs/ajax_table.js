
var ajax_table={
    props:['tab_head','par_row'],//['heads','row_filters','kw'],
    data:function(){
        var heads_ctx = this.tab_head.table_ctx
        return {
            heads:heads_ctx.heads,
            row_filters:heads_ctx.row_filters,
            row_sort:heads_ctx.row_sort,
            director_name:heads_ctx.director_name,
            footer:heads_ctx.footer || [],
            ops:heads_ctx.ops || [],
            rows:[],
            row_pages:{},
            //search_tip:this.kw.search_tip,

            selected:[],
            del_info:[],

            search_args: {}
        }
    },
    mixins:[mix_table_data,mix_ele_table_adapter],
    //watch:{
    //    // 排序变换，获取数据
    //    'row_sort.sort_str':function(v){
    //        this.search_args._sort=v
    //        this.get_data()
    //    }
    //},
    template:`<div class="rows-block flex-v" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 3em;" >
        <div class='flex' style="min-height: 3em;" v-if="row_filters.length > 0">
            <com-filter class="flex" :heads="row_filters" :search_args="search_args"
                        @submit="search()"></com-filter>
            <div class="flex-grow"></div>
        </div>

        <div  v-if="ops.length>0">
            <div class="oprations" style="padding: 5px">
                <component v-for="op in ops"
                           :is="op.editor"
                           :ref="'op_'+op.name"
                           :head="op"
                           :disabled="get_attr(op.disabled)"
                           v-show="! get_attr(op.hide)"
                           @operation="on_operation(op)"></component>
            </div>
        </div>

        <div class="box box-success flex-grow">
            <div class="table-wraper" style="position: absolute;top:0;left:0;bottom: 0;right:0;">
               <el-table class="table" ref="e_table"
                              :data="rows"
                              border
                              show-summary
                              :span-method="arraySpanMethod"
                              :fit="false"
                              :stripe="true"
                              size="mini"
                              @sort-change="sortChange($event)"
                              @selection-change="handleSelectionChange"
                              :summary-method="getSum"
                              height="100%"
                              style="width: 100%">

                        <template  v-for="head in heads">
                              <el-table-column
                                    v-if="head.type"
                                    :type="head.type"
                                    :width="head.width">
                              </el-table-column>

                            <el-table-column v-else-if="head.editor"
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
                                             :prop="head.name"
                                             :label="head.label"
                                             :sortable="is_sort(head)"
                                             :width="head.width">
                            </el-table-column>

                        </template>

                    </el-table>
            </div>

        </div>
          <div>
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
    </div>`,


    methods:{
        on_show:function(){
            if(! this.fetched){
                this.search()
                this.fetched = true
            }
        },
        getRows:function(){
        //
            var self=this
            if(self.tab_head.tab_field){
                self.search_args[self.tab_head.tab_field] = self.par_row[self.tab_head.par_field]
            }else{
                self.search_args[self.tab_head.par_field] = self.par_row[self.tab_head.par_field]
            }

            ex.vueSuper(self,{fun:'getRows'})
            //var fun = get_data[this.tab_head.get_data.fun ]
            //fun(function(rows,row_pages,footer){
            //    self.rows = rows
            //    self.row_pages =row_pages
            //    self.footer = footer
            //
            //},this.par_row,this.tab_head.get_data.kws,this.search_args)

    },
        add_new:function(kws){
            var self=this
            var inn_kws = ex.copy(kws)
            var init_fields={}
            if(self.tab_head.tab_field){
                init_fields[ self.tab_head.tab_field] = self.par_row[self.tab_head.par_field]
            }else{
                init_fields[self.tab_head.par_field]=self.par_row[self.tab_head.par_field]
            }
            var dc = {fun:'add_new',init_fields:init_fields }
            ex.assign(inn_kws,dc)
            ex.vueSuper(this,inn_kws)
        },
        arraySpanMethod:function({ row, column, rowIndex, columnIndex }){
            if(this.table_layout){
                return this.table_layout[`${rowIndex},${columnIndex}`] || [1,1]
            }else{
                return [1,1]
            }
            //var head = this.heads[columnIndex]

            //return [1,1]
        }
    }
}

Vue.component('com_tab_table',ajax_table)

//var get_data={
//    get_rows:function(callback,row,kws,search_args){
//        var relat_field = kws.relat_field
//        var director_name = kws.director_name
//
//        var self=this
//        var relat_pk = row[kws.relat_field]
//        var relat_field = kws.relat_field
//        search_args[relat_field] = relat_pk
//        var post_data=[{fun:'get_rows',search_args:search_args,director_name:director_name}]
//        cfg.show_load()
//        $.post('/d/ajax',JSON.stringify(post_data),function(resp){
//            cfg.hide_load()
//            callback(resp.get_rows.rows,resp.get_rows.row_pages,resp.get_rows.footer)
//            //self.rows = resp.get_rows.rows
//            //self.row_pages =resp.get_rows.row_pages
//        })
//    }
//}