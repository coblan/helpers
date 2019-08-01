require('./scss/table_grid.scss')
var ele_table= {
    props: ['bus'],
    created: function () {
        //this.bus.table = this

    },
    data: function () {
        this.parStore=ex.vueParStore(this)
        var keyed_heads ={}
        ex.each(this.parStore.heads,function(head){
            keyed_heads[head.name]=head
        })
        return {
            heads: this.parStore.heads,
            keyed_heads:keyed_heads,
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
        this.parStore.$on('data-updated-backend',this.on_data_updated)
        ex.each(this.parStore.heads,(head)=>{
            if(head.style){
                ex.append_css(head.style)
            }
        })
    },


    computed: {
        default_sort(){
            var sort_str = this.parStore.row_sort.sort_str
            if(!sort_str){
                return {}
            }
            var sort_list = sort_str.split(',')
            sort_str = sort_list[0]
            if(sort_str.startsWith('-') ){
                var prop=sort_str.slice(1)
                var order = 'descending'
            }else{
                var prop = sort_str
                var order = 'ascending'
            }
            return {prop: prop, order: order}
        },
        normed_heads(){
            var out_ls =[]
            ex.each(this.parStore.heads,(head)=>{
                if(head.show) {
                    if(! ex.eval(head.show,{ps:this.parStore,vc:this,head:head})  ){
                        return
                    }
                }
                out_ls.push(head)
            })
            return out_ls
        },
        rows:function(){
            return this.parStore.rows
        },
        selected:function(){
            return this.parStore.selected
        },
        footer:function(){
            return this.parStore.footer
        },

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
        },

    },

    mixins: [mix_table_data, mix_ele_table_adapter],
    template: `<div class="com-table-grid" style="position: absolute;top:0;left:0;bottom: 0;right:0;">
        <el-table class="table flat-head" ref="e_table"
                              :data="rows"
                               border
                              show-summary
                              :row-class-name="tableRowClassName"
                              :span-method="parStore.arraySpanMethod"
                              :fit="false"
                              :stripe="true"
                              :default-sort='default_sort'
                              size="mini"
                              height="100%"
                              style="width: 100%"
                              @header-dragend="on_header_dragend"
                              @sort-change="on_sort_change($event)"
                              @selection-change="parStore.handleSelectionChange"
                              :summary-method="getSum">

                        <el-table-column v-if="parStore.selectable"
                                type="selection"
                                width="55">
                        </el-table-column>
                        <template v-for="head in normed_heads">
                             <el-table-column v-if="head.children"
                                :label="head.label"
                                :key="head.name"
                                 :class-name="head.class">
                                   <el-table-column v-for="head2 in name2head(head.children)"
                                            :class-name="head2.class"
                                            :key="head2.name"
                                             :show-overflow-tooltip="parStore.is_show_tooltip(head2) "
                                              :fixed="head2.fixed"
                                             :label="head2.label"
                                             :prop="head2.name.toString()"
                                             :sortable="parStore.is_sort(head2)"
                                             :sort-orders="['ascending', 'descending']"
                                             :width="head2.width">
                                        <template  slot-scope="scope">
                                            <component :is="head2.editor"
                                                       @on-custom-comp="on_td_event($event)"
                                                       :row-data="scope.row" :field="head2.name" :index="scope.$index">
                                            </component>

                                        </template>

                                    </el-table-column>
                             </el-table-column>
                            <el-table-column v-else-if="! head.sublevel && head.editor"
                                              :class-name="head.class"
                                              :key="head.name"
                                             :show-overflow-tooltip="parStore.is_show_tooltip(head) "
                                              :fixed="head.fixed"
                                             :label="head.label"
                                             :prop="head.name.toString()"
                                             :sortable="parStore.is_sort(head)"
                                             :sort-orders="['ascending', 'descending']"
                                             :width="head.width">
                                <template  slot-scope="scope">
                                    <component :is="head.editor"
                                               @on-custom-comp="on_td_event($event)"
                                               :row-data="scope.row" :field="head.name" :index="scope.$index">
                                    </component>

                                </template>

                            </el-table-column>
                              <el-table-column v-else-if="! head.sublevel"
                                             :show-overflow-tooltip="parStore.is_show_tooltip(head) "
                                             :fixed="head.fixed"
                                             :key="head.name"
                                             :class-name="head.class"
                                             :prop="head.name.toString()"
                                             :label="head.label"
                                             :sortable="parStore.is_sort(head)"
                                             :sort-orders="['ascending', 'descending']"
                                             :width="head.width">
                            </el-table-column>

                        </template>
                    </el-table>
                    </div>`,
    methods: {
        on_header_dragend(newWidth, oldWidth, column, event){
            this.parStore.$emit('header-dragend',{newWidth:newWidth, oldWidth:oldWidth, column:column, event:event})
        },
        on_data_updated(){
            Vue.nextTick(()=>{
                this.$refs.e_table.doLayout()
            })
        },
        on_sort_change(event){
            if(this._sort_has_changed ){
                this.parStore.sortChange(event)
            }else if( event.order != this.default_sort.order || event.prop != this.default_sort.prop ) {
                this._sort_has_changed = true
                this.parStore.sortChange(event)
            }
        },
        name2head:function(name_list){
            var bb =  ex.map(name_list,(name)=>{
                return this.keyed_heads[name]
            })

            return ex.filter(bb,(item)=>{
                return Boolean(item)
            })

        },
        tableRowClassName:function({row, rowIndex}){
            var class_list =[]
            if(row._css_class){
                clss_list.push( row._css_class)
            }
            if(ex.isin(row,this.selected)){
                class_list.push('row-select')
            }
            return class_list.join(' ')

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
}
Vue.component('com-table-grid',ele_table)

var arg_filter={
    field:function(row,head){
        return row[head.field]
    }
}

Vue.component('com-element-table-colomu',{
    props:['head'],
    data:function(){
        var self=this
      return {
          parStore:ex.vueParStore(self)
      }
    },
    template:`<template >

                            <el-table-column v-if="head.editor"
                                             :show-overflow-tooltip="parStore.is_show_tooltip(head) "
                                              :fixed="head.fixed"
                                             :label="head.label"
                                             :prop="head.name.toString()"
                                             :sortable="parStore.is_sort(head)"
                                             :sort-orders="['ascending', 'descending']"
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
                                             :fixed="head.fixed"
                                             :prop="head.name.toString()"
                                             :label="head.label"
                                             :sortable="parStore.is_sort(head)"
                                             :sort-orders="['ascending', 'descending']"
                                             :width="head.width">
                            </el-table-column>

         </template>
    `
})

