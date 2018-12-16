var pop_table_select =  {
    props:['row','head'],
    template:`<div>
        <span  v-text="label"></span>
        <input type="text" v-model="row[head.name]" style="display: none;" :id="'id_'+head.name" :name="head.name">
        <span v-if="!head.readonly" class="clickable" @click="open_win"><i class="fa fa-search"></i></span>
    </div>`,
    computed:{
        label:function(){
            return this.row['_'+this.head.name+'_label']
        }
    },
    mounted:function(){
        //var self=this
        //var name =this.head.name
        //this.validator=$(this.$el).validator({
        //    fields: {
        //        name:'required;'
        //    }
        //})
    },
    methods:{
        open_win:function(){
            var self=this
            //pop_table_layer(this.row,this.head.table_ctx,function(foreign_row){
            //    Vue.set(self.row,self.head.name,foreign_row[self.head.name])
            //    Vue.set(self.row,'_'+self.head.name+'_label',foreign_row._label)
            //})
            var win_close = cfg.pop_middle('com-table-panel',this.head.table_ctx,function(foreign_row){
                    Vue.set(self.row,self.head.name,foreign_row[self.head.name])
                    Vue.set(self.row,'_'+self.head.name+'_label',foreign_row._label)
                win_close()
            })
        },
        //isValid:function(){
        //    return this.validator.isValid()
        //}
    }
}

Vue.component('com-field-pop-table-select',pop_table_select)