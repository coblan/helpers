require('./styl/list.styl')

Vue.component('com-ti-list',{
    props:['ctx'],
    template:`<div class="com-ti-list">
    <div v-if="rows.length!=0" class="list-rows">
        <component v-for="row in rows" :key="row.pk || row.id || row.name" :is="ctx.item_ctx.editor" :ctx="get_item_ctx(ctx.item_ctx,row)"></component>
    </div>
    <div v-else style="line-height: 400px;text-align: center">
        <span>暂无数据</span>
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
    </div>`,
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
        if(this.ctx.mounted_express){
            ex.eval(this.ctx.mounted_express,{vc:this,head:this.ctx})
        }else{
            // 老的调用,废弃
            this.search()
            if(this.ctx.on_mounted){
                ex.eval(this.ctx.on_mounted,{vc:this})
            }
        }


    },
    methods:{
    get_item_ctx(head,row){
        var dc={}
        ex.vueAssign(dc,head)
        dc.row=row
        return dc
        
    },
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
            var postdata={_page:this.row_pages.crt_page,_perpage:this.row_pages.perpage}
            if(this.ctx.preset){
                Object.assign(postdata, ex.eval( this.ctx.preset ) )
            }
            cfg.show_load()
            return ex.director_call(this.ctx.director_name,postdata).then((resp)=>{
                cfg.hide_load()
                this.rows = resp.rows
                this.row_pages = resp.row_pages
            })
        }
    }
})