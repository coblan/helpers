export function get_table_store(){
    var table_store={
        data(){
            let search_args = ex.parseSearch()
            search_args._page  = search_args._page || 1
            return {
                rows:[],
                director_name:'',
                search_args:search_args,
                parents:[],
                row_pages:{},

            }
        },
        methods:{
            search(){
                this.search_args._page=1

                return this.getRows()
            },
            filter_load_row(rows){
                return rows
            },
            getRows(){
                if(this.ctx.filter_express){
                    let env = ex.eval(this.ctx.filter_express,{ps:this})
                    ex.vueAssign(this.search_args, env)
                }
                var post_data=[{fun:'get_rows',director_name:this.director_name,search_args:this.search_args}]
                cfg.show_load()
                return ex.post('/d/ajax',JSON.stringify(post_data)).then(resp=> {
                    cfg.hide_load()
                    this.rows = this.filter_load_row( resp.get_rows.rows )
                    this.parents = resp.get_rows.parents
                    ex.vueAssign( this.row_pages,resp.get_rows.row_pages)
                    return this.rows
                })
            },
            addNextPage(){
                /**
                 * 无限加载时，需要不断的添加
                 */
                this.search_args._page += 1
                var post_data=[{fun:'get_rows',director_name:this.director_name,search_args:this.search_args}]
                return ex.post('/d/ajax',JSON.stringify(post_data)).then(resp=> {
                    var row_pages =  resp.get_rows.row_pages
                    var max_page = Math.ceil(row_pages.total / row_pages.perpage)
                    ex.vueAssign( this.row_pages,resp.get_rows.row_pages)
                    this.search_args._page = this.row_pages.crt_page
                    if(row_pages.crt_page< max_page){
                        var new_rows = resp.get_rows.rows
                    }else{
                        var space =  this.rows.length - (max_page-1)*row_pages.perpage
                        var new_rows = resp.get_rows.rows.slice(space)
                    }
                    new_rows = this.filter_load_row(new_rows)
                    this.rows = this.rows.concat(new_rows)
                    return new_rows
                })
            },
            newRow(_director_name,pre_set){
                var self = this
                let director_name = _director_name || this.director_name+'.edit'
                var dc = {fun:'get_row',director_name:director_name}
                if(pre_set){
                    var pre_set = ex.eval(pre_set,{ps:self})
                    ex.assign(dc,pre_set)
                }
                var post_data=[dc]
                cfg.show_load()
                return new Promise((resolve,reject)=>{
                    ex.post('/d/ajax',JSON.stringify(post_data)).then(resp=>{
                        cfg.hide_load()
                        resolve(resp.get_row)
                    })
                })
                //var resp = await ex.post('/d/ajax',JSON.stringify(post_data))
                //cfg.hide_load()
                //return resp.get_row
            },
            update_or_insert(new_row){
                var table_row = ex.findone(this.rows,{pk:new_row.pk})
                if(table_row){
                    ex.vueAssign(table_row,new_row)
                }else{
                    this.rows=[new_row].concat(this.rows)
                }
                this.$emit('row.update_or_insert',new_row)
            }
        }
    }
    return table_store
}
window.table_store= get_table_store()

