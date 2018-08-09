/*
 * root 层面创建Vue组件，形成弹出框
 * */

export  function pop_table_layer (row,table_ctx,callback){
    // row,head ->//model_name,relat_field


    var pop_id =new Date().getTime()

    var opened_layer_indx = layer.open({
        type: 1,
        area: ['800px', '500px'],
        title: '列表',
        resize:true,
        resizing: function(layero){
            var total_height= $('#pop-table-'+pop_id).parents('.layui-layer').height()
            $('#pop-table-'+pop_id).parents('.layui-layer-content').height(total_height-42)
            layer_vue.resize()
            layer_vue.setHeight(total_height-160)

        },
        shadeClose: true, //点击遮罩关闭
        content:`<div id="pop-table-${pop_id}" style="height: 100%;">

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
    });

    if(table_ctx.extra_mixins){
        var real_extra_mixins = ex.map(table_ctx.extra_mixins,function(item){
            if(typeof (item)=='string'){
                return window[item]
            }else{
                return item
            }
        })
        var mixins= [mix_table_data,mix_ele_table_adapter] .concat(real_extra_mixins)
    }else{
        var mixins= [mix_table_data,mix_ele_table_adapter]
    }
    if(table_ctx.selectable ==undefined ){
        table_ctx.selectable =true
    }

    var layer_vue = new Vue({
        el:'#pop-table-'+pop_id,

        data:{
            par_row:row,
            //table_ctx:table_ctx,
            table_ctx:table_ctx,
            heads:table_ctx.heads,
            selectable:table_ctx.selectable,

            row_filters:table_ctx.row_filters,
            row_sort:table_ctx.row_sort,
            director_name:table_ctx.director_name,
            row_pages:{},
            rows:[],
            footer:[],
            selected:[],
            del_info:[],
            search_args: {},

            height:350,
        },
        mixins:mixins,
        mounted:function(){
            this.getRows()
            //this.$refs.com_table.getRows()
            //var self =this
           //setTimeout(function(){
           //     self.$refs.com_table.getRows()
           // },1000)

            var self=this
            ex.assign(this.op_funs, {
                send_select: function (kws) {
                    // 用作选择框时，(只选择一个) 会用到该函数
                    callback(kws.row)
                    layer.close(opened_layer_indx)

                }
            })

        },
        methods:{
            setHeight:function(height){
                this.height=height
            }
            //on_sub_success:function(event){
            //    callback({name:'selected',row:event.row})
            //    //callback({name:'after_save',new_row:event.new_row,old_row:event.old_row})
            //
            //},

        }
    })
}

window.pop_table_layer = pop_table_layer