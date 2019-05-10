var table_store={
    data(){
        let search_args = ex.parseSearch()
        search_args._page  = search_args._page || 1
        return {
            rows:[],
            director_name:'',
            search_args:search_args,
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
        }

    }
}

window.table_store= table_store