
<template>
<div class="com-top-list">
    <div class="web-wrap">
        <component v-for="row in rows" :is="ctx.item_editor" :ctx="row"></component>
    </div>
    <div>
        <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="row_pages.crt_page"
                :page-sizes="[20, 50, 100]"
                :page-size="row_pages.perpage"
                layout="total, sizes, prev, pager, next, jumper"
                :total="row_pages.total">
        </el-pagination>
    </div>
</div>
</template>
<script>
export default {
    props:['ctx'],
    data(){
        var childStore = new Vue()
        childStore.vc=this
        return {
            childStore:childStore,
            rows:[],
            row_pages:{
                crt_page:1,
                total:0,
                perpage:20,

            },
        }
    },
    mounted(){
        this.search()
    },
    methods:{
        handleSizeChange(val){
            this.row_pages.perpage=val
            cfg.show_load()
            this.search().then(()=>{
                cfg.hide_load()
        })
        },
        handleCurrentChange(){

        },
        search(){
            this.row_pages.crt_page =1
            return this.get_rows()
        },
        get_rows(){
            return ex.director_call(this.ctx.director_name,{_page:this.row_pages.crt_page,_perpage:this.row_pages.perpage}).then((resp)=>{
                this.rows = resp.rows
            this.row_pages = resp.row_pages
        })
        }
    }
}
</script>
