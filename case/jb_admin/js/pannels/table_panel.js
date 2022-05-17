
export default {
    props:['ctx'],

    data:function(){
        var self =this
        if(this.ctx.selectable == undefined){
            this.ctx.selectable =true
        }
        var base_table_panel_store ={
            props:['ctx'],
            propsData: {
                ctx: self.ctx
            },
            data:function(){
                return {
                    head:self.ctx,
                    vc:self,
                    par_row:self.ctx.par_row || {},
                    heads:self.ctx.heads || [],
                    selectable:self.ctx.selectable,
                    search_args: self.ctx.search_args || {},
                    row_filters:self.ctx.row_filters || {},
                    row_sort:self.ctx.row_sort || {sortable:[]},
                    director_name:self.ctx.director_name || '',
                    ops:self.ctx.ops || [],
                    row_pages: self.ctx.row_pages || {crt_page:1,total:0,perpage:20},
                    rows:[],
                    footer:[],
                    selected:[],
                }
            },
            mixins:[table_store]
        }
        var this_table_store = this.get_custom_store(base_table_panel_store)
        //var this_table_store =  {
        //    mixins:[table_store,base_table_store].concat(custom_store)
        //}
        return {
            childStore:new Vue(this_table_store),
            par_row:this.ctx.par_row || {},
            del_info:[],
        }
    },
    mixins:  [mix_table_data,mix_ele_table_adapter],

    mounted:function(){
        this.childStore.$on('finish',this.emit_finish)
        if(this.ctx.event_slots){
            ex.vueEventRout(this,this.ctx.event_slots)
        }
        // 如果有复杂的需求，则被 table_store.init_express接管
        // TODO 2020/9/7 修改为 mounted_express ,可能有兼容性问题
        if(this.ctx.mounted_express){
            ex.eval(this.ctx.mounted_express,{vc:this})
        }else if(this.ctx.autoload || this.ctx.autoload ==undefined){
            this.childStore.search()
        }
        //if(!this.childStore.head.init_express){
        //    this.childStore.search()
        //}
    },
    methods:{
        get_custom_store:function(base_table_panel_store){
            return base_table_panel_store
        },
        emit_finish:function(event){
            this.$emit('finish',event)
        }
    },
    template:`<div class="com-table-panel" style="height: 100%;">

            <div class="rows-block flex-v" style="height: 100%">


              <div v-if="childStore.row_filters.length > 0" style="background-color: #fbfbf8;padding: 8px 1em;border-radius: 4px;margin-top: 8px">

                     <com-table-filters></com-table-filters>

               </div>

               <!--<div  v-if="childStore.ops.length>0 && childStore.tab_stack.length ==0">-->
               <div  v-if="childStore.ops.length>0">
                        <com-table-operations></com-table-operations>
               </div>

                <div class="box box-success flex-v flex-grow" style="margin-bottom: 0">
                    <div class="table-wraper flex-grow" style="position: relative;">

                        <com-table-rows></com-table-rows>
                    </div>
                </div>
            <div style="background-color: white;">
                <com-table-pagination></com-table-pagination>
            </div>

        </div>
    </div>`
}

// window.com_table_panel=table_panel
//Vue.component('com-table-editor',table_panel)

//window.com_table_panel=table_panel

