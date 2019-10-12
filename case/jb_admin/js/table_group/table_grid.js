require('./scss/table_grid.scss')
var ele_table= {
    props: ['ctx'],
    created: function () {
        //this.bus.table = this

    },
    data: function () {
        var parStore=ex.vueParStore(this)
        var keyed_heads ={}
        ex.each(parStore.heads,function(head){
            keyed_heads[head.name]=head
        })

        if(parStore.advise_heads && parStore.advise_heads.length > 0){
            var key = '_table_settings_'+parStore.director_name
            var setting_str = localStorage.getItem(key)
            if(setting_str){
                var setting_obj = JSON.parse(setting_str)
                setting_obj.advise_width  = setting_obj.advise_width || {}
                setting_obj.advise_order = setting_obj.advise_order || []
                ex.each(parStore.heads,(head)=>{
                    if( setting_obj.advise_width[head.name]){
                        head.width = setting_obj.advise_width[head.name]
                    }
                })
            }
            else{
                var setting_obj ={
                    advise_heads:parStore.advise_heads,
                    advise_width:{},
                    advise_order:[],
                }
                localStorage.setItem(key,JSON.stringify(setting_obj))
            }
            parStore.advise_heads = setting_obj.advise_heads
            parStore.advise_width = setting_obj.advise_width || {}
            parStore.advise_order= setting_obj.advise_order ||[]
        }else{
            parStore.advise_heads = []
            parStore.advise_width = {}
            parStore.advise_order = []
        }
        if(parStore.advise_order.length > 0 ){
            parStore.heads = ex.sort_by_names(parStore.heads , parStore.advise_order,true)
        }

        return {
            parStore:parStore,
            heads: parStore.heads,
            keyed_heads:keyed_heads,
            //rows:this.parStore.rows,
            search_args: parStore.search_args,
            row_sort: parStore.row_sort,
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
            if( this.parStore.advise_heads.length > 0){
                var left_heads = ex.filter(this.parStore.heads,(head)=>{
                    return ex.isin(head.name,this.parStore.advise_heads)
                })
            }else{
                var left_heads = this.parStore.heads
            }

            ex.each(left_heads,(head)=>{
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
        //footer:function(){
        //    return this.parStore.footer
        //},
    },
    watch:{
        selected:function(newvalue,old){
            if(newvalue.length==0 && old.length !=0){
                this.$refs.e_table.clearSelection()
            }else{
                ex.each(old,(row)=>{
                    if(newvalue.indexOf(row)==-1){
                        this.$refs.e_table.toggleRowSelection(row,false)
                    }
                })
                ex.each(newvalue,(row)=>{
                    if(old.indexOf(row)==-1){
                        this.$refs.e_table.toggleRowSelection(row,true)
                    }
                })
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
                                width="50">
                        </el-table-column>
                        <template v-for="(head,index) in normed_heads">
                             <el-table-column v-if="head.children"
                                :label="head.label"
                                :key="head.name"
                                 :class-name="head.class">
                                   <el-table-column v-for="head2 in name_in_list(head.children)"
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
                                                        :key="head2.name"
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
        getSum:function(param){
            var footer =[]
            if(this.parStore.selectable){
                footer.push(this.parStore.footer._label || '')
            }
            ex.each(this.normed_heads,(head)=>{
                if(head.children){
                    var subheads = this.name_in_list(head.children)
                    ex.each(subheads,(subhead)=>{
                        footer.push(this.parStore.footer[subhead.name] || '')
                    })
                }else if(! head.sublevel){
                    footer.push(this.parStore.footer[head.name] || '')
                }
            })
            return  footer
        },
        on_header_dragend(newWidth, oldWidth, column, event){
            this.parStore.$emit('header-dragend',{newWidth:newWidth, oldWidth:oldWidth, column:column, event:event})

            if(this.parStore.advise_heads && this.parStore.advise_heads.length >0){
                var key = '_table_settings_'+ this.parStore.director_name
                var setting_str = localStorage.getItem(key)
                var setting_obj = JSON.parse(setting_str)
                setting_obj.advise_width = setting_obj.advise_width || {}
                setting_obj.advise_width[column.property] = newWidth
                localStorage.setItem(key,JSON.stringify(setting_obj))
            }
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
        name_in_list:function(name_list){

             return ex.filter(this.normed_heads,(head)=>{
                return ex.isin(head.name,name_list)
            })
            //var heads_list = ex.filter(name_list,(name)=>{
            //   return ex.findone(this.normed_heads,{name:name})
            //})
            //var bb =  ex.map(heads_list,(name)=>{
            //    return this.keyed_heads[name]
            //})
            //return ex.filter(bb,(item)=>{
            //    return Boolean(item)
            //})
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

