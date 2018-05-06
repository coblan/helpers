var pop_table_select =  {
    props:['row','head'],
    template:`<div>
        <span v-if='head.readonly' v-text='label'></span>
        <span @click="open_win">xxx</span>
    </div>`,
    computed:{
        label:function(){
            return this.row['_'+this.head.name+'_label']
        }
    },
    methods:{
        open_win:function(){
            var self=this
            pop_table_layer(this.row,this.head.table_ctx,function(for_row){

                self.row[this.head_name]=for_row.pk
                self.row['_'+this.head.name+'_label'] = for_row._label
            })
        }
    }
}

Vue.component('com-field-pop-table-select',pop_table_select)