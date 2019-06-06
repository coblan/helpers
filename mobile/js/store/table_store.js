var table_store={
    data(){
        let search_args = ex.parseSearch()
        search_args._page  = search_args._page || 1
        return {
            rows:[],
            director_name:'',
            search_args:search_args,
            parents:[],

        }
    },
    methods:{
        search(){
            this.search_args._page=1
            return this.getRows()
        },
        getRows(){
            var post_data=[{fun:'get_rows',director_name:this.director_name,search_args:this.search_args}]
            return ex.post('/d/ajax',JSON.stringify(post_data)).then(resp=> {
                this.rows = resp.get_rows.rows
                this.parents = resp.get_rows.parents
            })
        },
        addNextPage(){
            this.search_args._page += 1
            var post_data=[{fun:'get_rows',director_name:this.director_name,search_args:this.search_args}]
            return ex.post('/d/ajax',JSON.stringify(post_data)).then(resp=> {
                var row_pages =  resp.get_rows.row_pages
                var max_page = Math.ceil(row_pages.total / row_pages.perpage)
                if(row_pages.crt_page< max_page){
                    this.rows = this.rows.concat(resp.get_rows.rows)
                }else{
                    var space =  this.rows.length - (max_page-1)*row_pages.perpage
                    this.rows = this.rows.concat(resp.get_rows.rows.slice(space))
                }
            })
        },
        async newRow(_director_name,pre_set){
            var self = this
            let director_name = _director_name || this.director_name+'.edit'
            var dc = {fun:'get_row',director_name:director_name}
            if(pre_set){
                var pre_set = ex.eval(pre_set,{ps:self})
                ex.assign(dc,pre_set)
            }
            var post_data=[dc]
            cfg.show_load()
            var resp = await ex.post('/d/ajax',JSON.stringify(post_data))
            cfg.hide_load()
            return resp.get_row
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

window.table_store= table_store