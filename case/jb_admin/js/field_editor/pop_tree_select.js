var pop_tree_select =  {
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
    },
    methods:{
        open_win:function(){
            var self=this
            cfg.pop_vue_com('com-pop-tree',this.head.tree_ctx).then(resp=>{
                if(self.head.after_select){
                    ex.eval(self.head.after_select,{selected_row:resp,row:self.row})
                }else{
                    Vue.set(self.row,self.head.name,resp.value)
                    Vue.set(self.row,'_'+self.head.name+'_label',resp.path)
                }
            })
        },
    }
}

Vue.component('com-field-pop-tree-select',pop_tree_select)


Vue.component('com-pop-tree',{
    props:['ctx'],
    template:`<div>
    <el-tree
          :data="ctx.options"
          :props="defaultProps"
          accordion
          @node-click="handleNodeClick">
       </el-tree>
    </div>`,
    data(){
        return {
            defaultProps: {
                children: 'children',
                label: 'label',
            }
        }
    },
    methods:{
        handleNodeClick(data){
            this.$emit('finish',{value:data.value,label:data.label,path:data.path})
        }
    }
})