<template>
    <div class="com-d-table flex-v">
        <dfilter :heads="filterHeads" @search="search_page(1)" :search-args="searchArgs"></dfilter>
        <d-operation :heads="operationHeads"></d-operation>
        <div class="box box-success flex-v flex-grow" style="margin-bottom: 0">
            <!--<div class="table-wraper flex-grow" >-->
                <dtable ref="dtable" class="my-d-table"
                        :heads="tableHeads"
                        :rows="tableRows"
                        :selected="selected"
                        :row-Sort="rowSort" :search-args="searchArgs"></dtable>
            <!--</div>-->
        </div>
        <dpagination :row-pages="rowPages" @goto-page="search_page($event)" :search-args="searchArgs"></dpagination>
    </div>
</template>
<script>
    import dtable from 'webcase/director/table/dtable.vue'
    import dOperation from 'webcase/director/table/doperation.vue'
    import dfilter from 'webcase/director/table/dfilter.vue'
    import dpagination from 'webcase/director/table/dpagination.vue'
    import table_mix from './director_table/table_mix'
    export default {
        components:{
            dtable,
            dfilter,
            dpagination,
            dOperation
        },
        mixins:[table_mix],
        props:{
            filterHeads:{
                default:()=>{return []}
            },
            searchArgs:{
                default:()=>{return {}}
            },
            tableRows:{
                default:()=>{return []}
            },
            tableHeads:{
                default:()=>{return []}
            },
            rowSort:{
                default:()=>{return {}}
            },
            rowPages:{
                default:()=>{return {}}
            },
            operationHeads:{
                default:()=>[]
            },
            directorName:{},

        },
        data (){
            var self =this

            let childStore = new Vue({
                computed:{
                    has_select(){
                        return self.selected.length !=0
                    }
                },
                methods:{
                    add_new(kws){
                        self.addNew(kws)
                    },
                    search(){
                        self.search_page(1)
                    },
                    check_selected(head){
                      return self.check_selected(head)
                    },
                    delete_selected(){
                        return self.delete_selected()
                    }
                }
            })
            childStore.vc = this
            window.vc = this
            return {
                selected:[],
                childStore:childStore,
            }
        },
        mounted(){
            this.$nextTick(()=>{
                this.childStore.selected = this.$refs.dtable.selected
            })
        },
        methods:{
            search(){
                this.search_page(1)
            },
            search_page(page){
                this.searchArgs._page = page
                cfg.show_load()
                ex.director_call('d.get_rows',{director_name:this.directorName,search_args:this.searchArgs}).then(resp=>{
                    cfg.hide_load()
                    this.tableRows.splice(0,this.tableRows.length,...resp.rows)
                    ex.vueAssign( this.rowPages,resp.row_pages)
                    ex.vueAssign(this.searchArgs,resp.search_args)

                })

//                ex.director_call('d.get_rows',post_data,function(resp){
//                    cfg.hide_load()
//                    self.selected = []
//                    self.rows = resp.rows
//                    ex.vueAssign( self.row_pages,resp.row_pages)
//                    ex.vueAssign(self.search_args,resp.search_args)
//                    self.footer=resp.footer
//                    self.parents=resp.parents
//                    self.table_layout=resp.table_layout
//                    if(self.after_get_rows){
//                        ex.eval(self.after_get_rows,{ps:self,resp:resp})
//                    }
//                    self.$emit('data-updated-backend')
//                    resolve(resp)
//                })

//                this.$refs.dtable.search()
            }
        }
    }
</script>
<style scoped lang="scss">
.com-d-table{
    height: 100%;
}
.my-d-table{
    position: absolute;
    height: 100%;
    width: 100%;
}
</style>