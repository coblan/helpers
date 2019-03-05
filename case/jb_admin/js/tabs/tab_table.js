

var tab_table={
    props:['tab_head','par_row'],
    data:function(){
        var vc = this
        var heads_ctx = this.tab_head.table_ctx
        var my_table_store ={
            data:function(){
                return {
                    heads:heads_ctx.heads,
                    row_filters:heads_ctx.row_filters,
                    row_sort:heads_ctx.row_sort,
                    director_name:heads_ctx.director_name,
                    footer:heads_ctx.footer || [],
                    ops:heads_ctx.ops || [],
                    rows:[],
                    row_pages:{},
                    selectable:heads_ctx.selectable==undefined? true:heads_ctx.selectable,
                    selected:[],
                    del_info:[],
                    search_args: {},
                    vc:vc,
                    parStore:ex.vueParStore(vc)
                }
            },
            mixins:[table_store],
            watch:{
                search_args:function(v){
                    console.log(v)
                }
            },
            methods:{
                switch_to_tab:function(kws){
                    this.parStore.switch_to_tab(kws)
                },
                getRows:function(){
                    if(vc.tab_head.pre_get){
                        var pre_set = ex.eval(vc.tab_head.pre_get,{par_row:vc.par_row})
                        ex.assign(this.search_args,pre_set)
                    }else if(vc.tab_head.tab_field){ // 下面是老的调用，
                        this.search_args[vc.tab_head.tab_field] = vc.par_row[vc.tab_head.par_field]
                    }else if(vc.tab_head.par_field){
                        this.search_args[vc.tab_head.par_field] = vc.par_row[vc.tab_head.par_field]
                    }
                    table_store.methods.getRows.call(this)

                },
            }
        }
        return {
            childStore:new Vue(my_table_store)
        }
        //return {
        //    parents:parents,
        //    page_label:page_label,
        //    heads:heads,
        //    rows:rows,
        //    row_filters:row_filters,
        //    row_sort:row_sort,
        //    row_pages:row_pages,
        //    director_name:director_name,
        //    footer:footer,
        //    ops:ops,
        //    search_args:search_args,
        //}
    },
    mounted:function(){
        this.childStore.search()
    },

    template:`<div class="com-tab-table flex-v" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 1em;">
       <div v-if="childStore.row_filters.length > 0" style="background-color: #fbfbf8;padding: 8px 1em;border-radius: 4px;margin-top: 8px">
            <com-table-filters></com-table-filters>
        </div>
        <div  v-if="childStore.ops.length>0 ">
            <com-table-operations></com-table-operations>
        </div>

        <div v-if="childStore.parents.length>0">
            <com-table-parents></com-table-parents>
        </div>

        <!--<ol v-if="parents.length>0" class="breadcrumb jb-table-parent">-->
            <!--<li v-for="par in parents"><a href="#" @click="get_childs(par)"  v-text="par.label"></a></li>-->
        <!--</ol>-->

        <div class="box box-success flex-v flex-grow" style="margin-bottom: 0">
            <div class="table-wraper flex-grow" style="position: relative;">
                <com-table-grid></com-table-grid>
               </div>
        </div>
        <div style="background-color: white;">
            <com-table-pagination></com-table-pagination>
        </div>
    </div>`
}

Vue.component('com-tab-table',tab_table)