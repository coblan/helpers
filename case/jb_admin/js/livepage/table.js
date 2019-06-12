var live_table ={
    props:['ctx'],
    basename:'live-table',
    template:`<div class="live-table">
    hello table
    </div>`
}


var live_table={
    props:['ctx'],
    basename:'live-table',
    //props:['tab_head','par_row'],
    data:function(){
        var vc = this
        //var heads_ctx = this.ctx
        var my_table_store ={
            data:function(){
                return {
                    heads:vc.ctx.heads,
                    row_filters:vc.ctx.row_filters,
                    row_sort:vc.ctx.row_sort,
                    director_name:vc.ctx.director_name,
                    footer:vc.ctx.footer || [],
                    ops:vc.ctx.ops || [],
                    rows:[],
                    row_pages:{},
                    selectable:vc.ctx.selectable==undefined? true:vc.ctx.selectable,
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
                //switch_to_tab:function(kws){
                //    this.parStore.switch_to_tab(kws)
                //},
                //getRows:function(){
                //    if(vc.tab_head.pre_set){
                //        var pre_set = ex.eval(vc.tab_head.pre_set,{par_row:vc.par_row})
                //        ex.assign(this.search_args,pre_set)
                //    }else if(vc.tab_head.tab_field){ // 下面是老的调用，
                //        this.search_args[vc.tab_head.tab_field] = vc.par_row[vc.tab_head.par_field]
                //    }else if(vc.tab_head.par_field){
                //        this.search_args[vc.tab_head.par_field] = vc.par_row[vc.tab_head.par_field]
                //    }
                //    table_store.methods.getRows.call(this)
                //
                //},
            }
        }
        return {
            childStore:new Vue(my_table_store),
            parStore:ex.vueParStore(vc),
        }
    },
    mounted:function(){
        if(this.ctx.event_slots){
            ex.vueEventRout(this,this.ctx.event_slots)
        }
        this.childStore.search()
    },

    template:`<div class="live-table flex-v" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 1em;">
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




window.live_table = live_table