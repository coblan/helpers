
var cus_easytable={
    props:['rows','ctx'],
    data:function(){
        return {
            heads:this.ctx.heads,
            rows:this.ctx.rows,
            row_filters:this.ctx.row_filters,
            row_sort:this.ctx.row_sort,
            row_pages:this.ctx.row_pages,
            selected:[],
            search_args:ex.parseSearch(),
            ops:this.ctx.ops,
            crt_row:{},
        }
    }
}