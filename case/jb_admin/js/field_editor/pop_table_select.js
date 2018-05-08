var pop_table_select =  {
    props:['row','head'],
    template:`<div>
        <span v-if='head.readonly' v-text='label'></span>
        <span  v-text="label"></span>
        <span class="clickable" @click="open_win"><i class="fa fa-search"></i></span>
    </div>`,
    computed:{
        label:function(){
            return this.row['_'+this.head.name+'_label']
        }
    },
    methods:{
        open_win:function(){
            var self=this
            pop_table_layer(this.row,this.head.table_ctx,function(foreign_row){

                self.row[self.head.name]=foreign_row.pk
                self.row['_'+self.head.name+'_label'] = foreign_row._label
            })
        }
    }
}

Vue.component('com-field-pop-table-select',pop_table_select)