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

        <div class="rows-block">
        <div class='flex' style="min-height: 3em;" v-if="row_filters.length > 0">
            <com-filter class="flex" :heads="row_filters" :search_args="search_args"
                        @submit="search()"></com-filter>
            <div class="flex-grow"></div>
        </div>
        <div class="box box-success">
            <div class="table-wraper">
                <v-table ref="vtable"
                         is-horizontal-resize
                         is-vertical-resize
                         :title-row-height="30"
                         :vertical-resize-offset="80"
                         :row-height="24"
                         odd-bg-color="#f0f6f8"
                         column-width-drag
                         style="width: 100%;"
                         :height=height
                         :columns="columns"
                         :table-data="rows"
                         @sort-change="sortChange"
                         @on-custom-comp="on_td_event($event)"
                         row-hover-color="#eee"
                         row-click-color="#edf7ff">
                </v-table>
            </div>
            <div style="margin-top: 10px;">
                <v-pagination @page-change="get_page($event)"
                              :total="row_pages.total"
                              size="small"
                              :page-size="row_pages.perpage"
                              @page-size-change="on_perpage_change($event)"
                              :layout="['total', 'prev', 'pager', 'next', 'sizer', 'jumper']">
                </v-pagination>
            </div>
        </div>
    </div>
                    <!--<com-v-table ref="com_table"-->
                        <!--@del_success="on_del()"-->
                        <!--@sub_success="on_sub_success($event)"-->
                        <!--:par_row="par_row" :table_ctx="table_ctx">-->
                    <!--</com-v-table>-->
                </div>`
    });


    var layer_vue = new Vue({
        el:'#pop-table-'+pop_id,
        data:{
            par_row:row,
            //table_ctx:table_ctx,

            heads:table_ctx.heads,
            row_filters:table_ctx.row_filters,
            row_sort:table_ctx.row_sort,
            director_name:table_ctx.director_name,
            row_pages:{},
            rows:[],
            selected:[],
            del_info:[],
            search_args: {},

            height:350,
        },
        mixins:[mix_table_data,mix_v_table_adapter],
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
                    //callback({name:'selected',row:kws.row})
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