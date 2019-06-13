
var live_table_type={
    props:['ctx'],
    basename:'live-chart',
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
        if(this.ctx.autoload){
            this.childStore.search()
        }
    },

    template:`<div class="live-table flex-v" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 2px;">
       <div v-if="childStore.row_filters.length > 0" style="background-color: #fbfbf8;padding: 8px 1em;border-radius: 4px;margin-top: 8px">
            <com-table-filters></com-table-filters>
        </div>
        <div  v-if="childStore.ops.length>0 ">
            <com-table-operations></com-table-operations>
        </div>

        <div v-if="childStore.parents.length>0">
            <com-table-parents></com-table-parents>
        </div>
        <div class="box box-success flex-v flex-grow" style="margin-bottom: 0">
            <div class="table-wraper flex-grow" style="position: relative;">
                <!--<com-table-grid></com-table-grid>-->
                <div style="position: absolute;top:0;left: 0;bottom: 0;right: 0;overflow: auto">
                    <component :is="ctx.content_editor"></component>
                </div>
               </div>
        </div>
        <!--<div style="background-color: white;">-->
            <!--<com-table-pagination></com-table-pagination>-->
        <!--</div>-->
    </div>`
}


window.live_table_type = live_table_type