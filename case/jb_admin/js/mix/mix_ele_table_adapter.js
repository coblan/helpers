require('./scss/mix_ele_table_adapter.scss')

var mix_ele_table_adapter = {
    mounted:function(){
        if(!this.search_args._sort){
            Vue.set(this.search_args,'_sort','')
        }
    },
    watch:{
        'search_args._sort':function(v){
            if(!v && this.$refs.e_table){
                this.$refs.e_table.clearSort()
            }
        }
    },
    methods:{
        is_sort:function(head){
            if(ex.isin(head.name,this.row_sort.sortable)) {
                return 'custom'
            }else{
                return false
            }
        },
        is_show_tooltip:function(head){
            if(head.show_tooltip ==undefined){
                return true
            }else {
                return head.show_tooltip
            }
        },
        handleSelectionChange(val) {
            this.selected = val;
        },
        clearSelection:function(){
            this.selected =[]
            this.$refs.e_table.clearSelection()
        },
        sortChange(params){
            //{ column, prop, order }
            var self=this
//                this.$refs.e_table.clearSort()
//                ex.each(this.row_sort.sortable,function(name){
            if(params.prop){
                if(params.order=='ascending'){
                    self.search_args._sort=params.prop
                }else if(params.order=='descending'){
                    self.search_args._sort='-'+params.prop
                }
            }else{
                self.search_args._sort=''
            }
            this.search()
//                })

        },
        //getSum:function(param){
        //    return this.footer
        //},
        on_perpage_change:function(perpage){
            this.search_args._perpage=perpage
            this.search_args._page=1
            this.getRows()
        },
    }
}

window.mix_ele_table_adapter = mix_ele_table_adapter