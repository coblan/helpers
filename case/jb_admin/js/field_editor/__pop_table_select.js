var pop_table_select =  {
    props:['row','head'],
    template:`<div class="com-field-pop-table-select">

        <input type="text" v-model="row[head.name]" style="display: none;" :id="'id_'+head.name" :name="head.name">

<div style="min-width: 200px;min-height: 32px;background: white;border: 1px solid grey">
  <el-tag :closable=" can_clear" v-if="row[head.name]" @close="clear()">
    <span  v-text="label"></span>
  </el-tag>
</div>

    <span v-if="!head.readonly" class="clickable" @click="open_win"><i class="fa fa-search"></i></span>
         <!--<span v-if="show_search" class="clickable" @click="open_win"><i class="fa fa-search"></i></span>-->
    </div>`,
    computed:{
        label:function(){
            return this.row['_'+this.head.name+'_label']
        },
        can_clear(){
            if(this.head.readonly){
                return false
            }
            if(this.head.clearable==undefined){
                return true
            }else{
                return this.head.clearable
            }
        },
        show_search(){
            if(this.head.readonly){
                return false
            }else if(this.head.clearable==false ){
                return true
            }else{
                return !Boolean(this.row[this.head.name])
            }
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
        if(this.head.mounted_express){
            ex.eval(this.head.mounted_express,{vc:this,head:this.head,row:this.row})
        }
    },
    methods:{
        clear(){
            if(this.head.clear_express){
                ex.eval(this.head.clear_express,{head:this.head,row:this.row})
            }else{
                Vue.delete(this.row,this.head.name)
                Vue.delete(this.row,'_'+this.head.name+'_label')
                //this.row[this.head.name] = null
            }
        },
        open_win:function(){
            var self=this
            if(this.head.init_express || this.head.pop_express){
                // init_express 老的调用方式
                var pop_express = this.head.pop_express || this.head.init_express
                ex.eval(this.head.pop_express,{head:this.head,row:this.row})
            }
            cfg.pop_vue_com( 'com-backend-table'/*'com-table-panel'*/,this.head.table_ctx).then(foreign_row=>{
                    if(!foreign_row){
                        console.log('break table panel')
                        return
                    }
                    
                    Vue.set(self.row,'_'+self.head.name+'_label',foreign_row._label)
                    Vue.set(self.row,self.head.name,foreign_row.pk)
                    
                    var after_select_express = self.head.after_select_express||self.head.after_select
                    if(after_select_express){
                        ex.eval(after_select_express,{selected_row:foreign_row,row:self.row})
                    }else if(self.head.select_field){
                        Vue.set(self.row,self.head.name,foreign_row[self.head.select_field])
                    }
                    
            }).catch(()=>{
                console.log('break table panel')
            })
        },
    }
}

Vue.component('com-field-pop-table-select',pop_table_select)