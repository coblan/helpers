require('./scss/ele_tree_name_layer.scss')
var label_shower =  {
    props:['row','head'],

    methods:{
        check_depend:function(node){
            var self=this
            if(node.depend_list){
                ex.each(node.depend_list,function(dep_node){
                    self.$refs.et.setChecked(dep_node.value,true)
                    self.check_depend(dep_node)
                })
            }
        },
        walk_check_depend:function(node){
            var self=this
            if(!node.children){
                this.check_depend(node)
            }else{
                ex.each(node.children,function(item){
                    self.walk_check_depend(item)
                })
            }
        },
        uncheck_depended:function(node){
            var self=this
            if(node.depended_list){
                ex.each(node.depended_list,function(dep_node){
                    self.$refs.et.setChecked(dep_node.value,false)
                    self.uncheck_depended(dep_node)
                })
            }
        },
        walk_uncheck_depended:function(node){
            var self=this
            if(!node.children){
                this.uncheck_depended(node)
            }else{
                ex.each(node.children,function(item){
                    self.walk_uncheck_depended(item)
                })
            }
        },
        handleCheckChange(data, checked, indeterminate) {
            console.log(data, checked, indeterminate);

        },
        handleNodeClick(data) {
            //this.last_click=data
            //console.log(data);
        },
        handleCheck:function(data,e){
            console.log(data);
            var self=this
            if( ! data.children){
                var check = ex.isin(data,e.checkedNodes)
                if(check){
                    self.check_depend(data)
                }else {
                    self.uncheck_depended(data)
                }
            }else{
                var check = ex.isin(data,e.checkedNodes) || ex.isin(data,e.halfCheckedNodes)
                if(check){
                    self.walk_check_depend(data)
                }else{
                    self.walk_uncheck_depended(data)
                }
            }

            var ls =this.$refs.et.getCheckedKeys()
            ls =ex.filter(ls,function(itm){
                return itm!=undefined
            })
            this.row[this.head.name] = ls



            //var self=this
            //if(ex.isin(data,e.halfCheckedNodes)){
            //
            //    if(data.children){
            //
            //        var grand_childrens=[]
            //        ex.walk(data.children,function(opt){
            //            grand_childrens.push(opt)
            //        })
            //
            //        //self.update_checked(data)
            //        ex.walk(data.children,function(opt){
            //            self.update_checked(opt,grand_childrens)
            //        })
            //    }
            //}
            //
            //
            //var ls =this.$refs.et.getCheckedKeys()
            //
            //ls =ex.filter(ls,function(itm){
            //    return itm!=undefined
            //})
            //
            //var org_ls = self.row[self.head.name]
            //
            //var added_item = ex.filter(ls,function(item){
            //    return ! ex.isin(item,org_ls)
            //})
            //
            //ex.each(added_item,function(value){
            //    if(self.depend[value]){
            //        ex.each(self.depend[value],function(opt){
            //            ex.remove(opt.depend,value)
            //        })
            //    }
            //})
            //
            //var subtract_item = ex.filter(org_ls,function(item){
            //    return ! ex.isin(item,ls)
            //})
            //ex.each(subtract_item,function(value){
            //    if(self.depend[value]){
            //        ex.each(self.depend[value],function(opt){
            //            if(!ex.isin(value,opt.depend)){
            //                opt.depend.push(value)
            //            }
            //        })
            //    }
            //})
            //var final_list = ex.filter(ls,function(value){
            //    for(var i=0;i<self.has_depend_list.length;i++){
            //        var depend_opt = self.has_depend_list[i]
            //        if(depend_opt.value==value && depend_opt.depend.length>0){
            //            return false
            //        }
            //    }
            //    return true
            //})
            //
            //
            //this.update_disable()
            //self.$refs.et.setCheckedKeys(final_list)
            //self.row[self.head.name] = final_list

        },
        //update_disable:function(){
        //    var self=this
        //    ex.each(this.has_depend_list,function(opt){
        //        if(opt.depend.length >0){
        //            Vue.set(opt,'disabled',true)
        //            //self.$refs.et.getCheckedKeys().
        //            //opt.disableb=true
        //        }else{
        //            Vue.set(opt,'disabled',false)
        //        }
        //    })
        //},
        //update_checked:function(node,valid_node_list){
        //    var self=this
        //    var depend_node_list=self.depend[node.value]
        //    if(depend_node_list){
        //        ex.each(depend_node_list,function(depend_node){
        //            if(ex.isin(depend_node,valid_node_list) && self.is_depend_full_checked(depend_node)){
        //                self.$refs.et.setChecked(depend_node.value,true,true)
        //            }
        //        })
        //    }
        //    this.update_disable()
        //},
    },
    mounted:function(){
        var self=this
        self.depend={}
        self.has_depend_list=[]

        var options_dict ={}
        ex.walk(this.inn_head.options,function(opt){
            if(opt.value){
                options_dict[opt.value] = opt
            }
        })

        ex.walk(this.inn_head.options,function(opt){
            if(!opt.depend){
                return
            }
            opt.depend_list=[]

            ex.each( opt.depend,function(item_name){
                var item = options_dict[item_name]
                opt.depend_list.push(item)
                if(!item.depended_list){
                    item.depended_list = []
                }
                item.depended_list.push(opt)
            })
        })
    },
    data:function(){
        var inn_head=ex.copy(this.head)
        return {
            inn_head:inn_head,
            defaultProps: {
                children: 'children',
                label: 'label',
            }
        }
    },
    template:`<div class="com-field-ele-tree-name-layer">
        <el-tree ref="et" :data="inn_head.options" :props="defaultProps"
             @node-click="handleNodeClick"
             @check="handleCheck"
             show-checkbox
             @check-change="handleCheckChange"
             :default-checked-keys="row[head.name]"
             node-key="value"
    >
      <span class="custom-tree-node" slot-scope="{ node, data }">
        <span :title="data.help_text" v-text="node.label"></span>
      </span>

    </el-tree>
    </div>`,
    //default-expand-all
    computed:{
        label:function(){
            return this.row['_'+this.head.name+'_label']
        }
    }
}

Vue.component('com-field-ele-tree-depend',label_shower)
//Vue.component('com-field-ele-tree-name-layer',function(resolve,reject){
//ex.load_css('https://unpkg.com/element-ui/lib/theme-chalk/index.css')
//ex.load_js('https://unpkg.com/element-ui/lib/index.js',function(){
//resolve(label_shower)
//})
//})