<template>
    <div class="com-d-table flex-v">
        <dfilter :heads="filterHeads" @search="search_page(1)" :search-args="searchArgs"
        :search-label="seach_label"></dfilter>
        <d-operation :heads="operationHeads"></d-operation>
        <dparent :parents="parents" @click-parent="getChilds($event)"></dparent>
        <div class="box box-success flex-grow" style="margin-bottom: 0">
            <!--flex-v flex-grow-->
            <!--<div class="table-wraper flex-grow" >-->
                <dtable ref="dtable" class="my-d-table"
                        :heads="tableHeads"
                        :adviseHeads="adviseHeads"
                        :directorName="directorName"
                        :rows="tableRows"
                        :selected="selected"
                        :footer="footer"
                        @search="search_page(1)"
                        @sort-changed="sortChange"
                        :row-sort="rowSort" ></dtable>
            <!--</div>   :search-args="searchArgs"-->
        </div>
        <dpagination :row-pages="rowPages" @goto-page="search_page($event)" :search-args="searchArgs"></dpagination>
    </div>
</template>
<script>
    const { ref, reactive,computed ,onMounted,getCurrentInstance } = VueCompositionAPI

    import dtable from 'webcase/director/table/dtable.vue'
    import dOperation from 'webcase/director/table/doperation.vue'
    import dfilter from 'webcase/director/table/dfilter.vue'
    import dpagination from 'webcase/director/table/dpagination.vue'
    import table_mix from './director_table/table_mix'
    import dparent from 'webcase/director/table/dparent.vue'

    /*
    *
    * table_settings原理
    *
    *参与组件:导入的dtable,cfg.pop_vue_com弹出的dsetings(com-d-table-setting)组件
    * dtable 启动时，判断传入的adviseHeads如果不为空，就在localstoreage里面加载advise配置，并初始化自身的advise_heads,advise_order给norm_heads调用
    *点击按钮弹出dsetting界面，dsetting从table_ps拿到director_name和总的heads,advise_heads_cookie_path,读取localstorage配置初始化自己的advise_heads,advise_order
    * 修改配置后保存到localstorage,如果有advise_heads_cookie_path,则把advise_heads写入cookies
    *
    * 经过table_ps路由调用dtable.reloadAdviseInfo(),从localstorage重新加载配置，初始化advise_heads等参数
    * 如果遇到与原始adviseHeads中不存在的head,这触发@search时间
    *
    * com-d-table接受到@search事件，触发重新加载数据
    *
    * */

    class DTableLogic{
        setup(porps){
            const vc = getCurrentInstance()

            return {
            }
        }
        setParStore(vc){
            var self = vc
            let childStore = new Vue({
                data(){
                    return {
                        name:'d-table-store'
                    }
                },
                computed:{
                    search_args(){
                        debugger
                        return vc.props.searchArgs
                    },
                    has_select(){
                        debugger;
                        return self.selected.length !=0
                    },
                    selected:{
                        get(){
                            return self.selected
                        },
                        set(v){
                            self.selected = v
                        }
                    },
                    heads:{
                        get(){
                            debugger
                            return self.tableHeads
                        },
                        set(v){
                            // tableSetting组件里面会闪一下，刷新界面
                            ex.arrayReplace(self.tableHeads,v)
//                            self.tableHeads = v
                        }
                    },
                    advise_heads(){
                        return vc.adviseHeads // .$refs.dtable.advise_heads
                    },
                    advise_heads_cookie_path(){
                        return vc.adviseHeadsCookiePath
                    },
                    advise_order(){
                        return vc.$refs.dtable.advise_order
                    },
                    director_name(){
                        return vc.directorName
                    },
                    rows:{
                        get(){
                            return vc.tableRows
                        },
                        set(v){
                            ex.array.replace(vc.tableRows,v)
//                            vc.tableRows=v
                        }
                    }
                },
                methods:{
                    export_excel(head){
                        self.exportExcel(head)
                    },
                    switch_to_tab(kws){
                        self.switchToTab(kws)
                    },
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
                    },
                    selected_set_and_save(kws){
                        return self.selected_set_and_save(kws)
                    },
                    reloadAdviseInfo(){
                        self.$refs.dtable.reloadAdviseInfo()
                    },
                    getChilds(par){
                        self.getChilds(par)
                    }
                }
            })
            childStore.vc = vc
            return childStore
        }
    }

    export default {
        components:{
            dtable,
            dfilter,
            dpagination,
            dOperation,
            dparent,
        },
        mixins:[table_mix],
        setup(props){
            if(props.extendLogic){
                return props.extendLogic
            }else{
                return  {} //new DTableLogic().setup(props)
            }
        },
        props:{
            extendLogic:{},
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
            adviseHeads:{
                default:()=>[]
            },
            adviseHeadsCookiePath:{},
            rowPages:{
                default:()=>{return {}}
            },
            operationHeads:{
                default:()=>[]
            },
            directorName:{},
            footer:{
                default:()=>{}
            },
            parents:{
                default:()=>[]
            }

        },
        data (){
        var vc = this
        var logic = new DTableLogic()
            return {
                selected:[],
                childStore: logic.setParStore(vc) //childStore,
            }
        },
        mounted(){
//            this.$nextTick(()=>{
//                this.childStore.selected = this.$refs.dtable.selected
//            })
        },
        computed:{
            seach_label(){
                return cfg.tr.search
            }
        },
        methods:{

            search_page(page){
                this.searchArgs._page = page
                cfg.show_load()
                this.searchArgs._advise_heads= this.$refs.dtable.advise_heads
                ex.director_call('d.get_rows',{director_name:this.directorName,search_args:this.searchArgs}).then(resp=>{
                    cfg.hide_load()
//                    this.tableRows.splice(0,this.tableRows.length,...resp.rows)
                    ex.array.replace(this.tableRows,resp.rows)
                    ex.vueAssign( this.rowPages,resp.row_pages)
                    ex.vueAssign(this.searchArgs,resp.search_args)
                    ex.vueAssign(this.footer,resp.footer)
                    ex.array.replace(this.parents,resp.parents)
//                    this.footer = resp.footer
                })
            }
        }
    }
</script>
<style scoped lang="scss">
.com-d-table{
    height: 100%;
}
.my-d-table{
    /*position: absolute;*/
    /*height: 100%;*/
    /*width: 100%;*/
}
</style>