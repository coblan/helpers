var pop_table_select =  {
    props:['row','head'],
    template:`<div>

        <input type="text" v-model="row[head.name]" style="display: none;" :id="'id_'+head.name" :name="head.name">

  <el-tag :closable="!head.readonly" v-if="row[head.name]" @close="clear()">
   <span  v-text="label"></span>
</el-tag>
    <span v-if="!head.readonly" class="clickable" @click="open_win"><i class="fa fa-search"></i></span>
        <!--<span v-if="!head.readonly && ! row[head.name]" class="clickable" @click="open_win"><i class="fa fa-search"></i></span>-->
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
        clear(){
            this.row[this.head.name] = null
        },
        open_win:function(){
            var self=this
            if(this.head.init_express){
                ex.eval(this.head.init_express,{head:this.head,row:this.row})
            }
            cfg.pop_vue_com('com-table-panel',this.head.table_ctx).then(foreign_row=>{
                    if(!foreign_row){
                        console.log('break table panel')
                        return
                    }
                    if(self.head.after_select){
                        ex.eval(self.head.after_select,{selected_row:foreign_row,row:self.row})
                    }else if(self.head.select_field){
                        Vue.set(self.row,self.head.name,foreign_row[self.head.select_field])
                    }else{
                        Vue.set(self.row,self.head.name,foreign_row.pk)
                    }
                    Vue.set(self.row,'_'+self.head.name+'_label',foreign_row._label)
            }).catch(()=>{
                console.log('break table panel')
            })
            //var win_close = cfg.pop_middle('com-table-panel',this.head.table_ctx,function(foreign_row){
            //    if(self.head.action){
            //        ex.eval(self.head.action,{new_row:foreign_row,row:self.row})
            //    }else if(self.head.select_field){
            //        Vue.set(self.row,self.head.name,foreign_row[self.head.select_field])
            //    }else{
            //        Vue.set(self.row,self.head.name,foreign_row[self.head.name])
            //    }
            //        Vue.set(self.row,'_'+self.head.name+'_label',foreign_row._label)
            //    win_close()
            //})
        },
        //isValid:function(){
        //    return this.validator.isValid()
        //}
    }
}

Vue.component('com-field-pop-table-select',pop_table_select)