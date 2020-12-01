

var tab_table={
    props:['tab_head','par_row'],
    data:function(){
        var vc = this
        var heads_ctx = this.tab_head.table_ctx
        var my_table_store ={
            data:function(){
                return {
                    head:heads_ctx,
                    heads:heads_ctx.heads,
                    row_filters:heads_ctx.row_filters,
                    row_sort:heads_ctx.row_sort,
                    director_name:heads_ctx.director_name,
                    footer:heads_ctx.footer || [],
                    ops:heads_ctx.ops || [],
                    rows:[],
                    row_pages:{},
                    selectable:heads_ctx.selectable==undefined? true:heads_ctx.selectable,
                    advise_heads:heads_ctx.advise_heads || [],
                    selected:[],
                    del_info:[],
                    search_args: heads_ctx.search_args || {},
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
                    if(window.root_live){
                        table_store.methods.switch_to_tab(kws)
                    }else{
                        this.parStore.switch_to_tab(kws)
                    }
                },
                getRows:function(){
                    if(vc.tab_head.filter_express){
                        var search_filter = ex.eval(vc.tab_head.filter_express,{par_row:vc.par_row,vc:vc,ps:this})
                        ex.assign(this.search_args,search_filter)
                    }else if(vc.tab_head.pre_set){
                            // pre_set 含义不够清晰，被 filter_express 替代了
                        var pre_set = ex.eval(vc.tab_head.pre_set,{par_row:vc.par_row,vc:vc,ps:this})
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
            childStore:new Vue(my_table_store),
            parStore:ex.vueParStore(vc),
            loaded:false,
        }
    },
    mounted(){
        ex.vueEventRout(this,this.tab_head.event_slots)
        // 如果有复杂的需求，则被 table_store.init_express接管
        if(!this.childStore.head.init_express){
            Vue.nextTick(()=>{
                this.childStore.search()
            })
        }

        if(this.tab_head.mounted_express){
            ex.eval(this.tab_head.mounted_express,{vc:this,ps:this.parStore,cs:this.childStore,par_row:this.par_row})
        }

    },
    methods:{
        on_show:function (){
            // 如果有复杂的需求，则被 table_store.init_express接管
            //if(this.childStore.head.init_express){
            //    return
            //}
            //// TODO 下面的加载方式可能不需要了，因为tab是lazy加载,在mounted hook函数中可以达到同样功能，后面需要花时间移除该函数
            //if(! this.loaded ){
            //    this.childStore.search()
            //    this.loaded=true
            //}
        }
    },

    template:`<div class="com-tab-table flex-v" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 1em;">
       <div v-if="childStore.row_filters.length > 0"
       style="background-color: #fbfbf8;padding: 2px 1em;border-radius: 4px;">
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
                <com-table-rows></com-table-rows>
               </div>
        </div>
        <div style="background-color: white;">
            <com-table-pagination></com-table-pagination>
        </div>
    </div>`
}

Vue.component('com-tab-table',tab_table)