require('./scss/ele_tree_name_layer.scss')
var label_shower =  {
    props:['row','head'],

    methods:{
        handleCheckChange(data, checked, indeterminate) {
            console.log(data, checked, indeterminate);
            var self=this

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
        handleNodeClick(data) {

            //console.log(data);
        },
        handleCheck:function(data,e){
            console.log(data);
            var self=this
            if(ex.isin(data,e.halfCheckedNodes)){

                if(data.children){

                    var grand_childrens=[]
                    ex.walk(data.children,function(opt){
                        grand_childrens.push(opt)
                    })

                    //self.update_checked(data)
                    ex.walk(data.children,function(opt){
                        self.update_checked(opt,grand_childrens)
                    })
                }
            }


            var ls =this.$refs.et.getCheckedKeys()

            ls =ex.filter(ls,function(itm){
                return itm!=undefined
            })

            var org_ls = self.row[self.head.name]

            var added_item = ex.filter(ls,function(item){
                return ! ex.isin(item,org_ls)
            })

            ex.each(added_item,function(value){
                if(self.depend[value]){
                    ex.each(self.depend[value],function(opt){
                        ex.remove(opt.depend,value)
                    })
                }
            })

            var subtract_item = ex.filter(org_ls,function(item){
                return ! ex.isin(item,ls)
            })
            ex.each(subtract_item,function(value){
                if(self.depend[value]){
                    ex.each(self.depend[value],function(opt){
                        if(!ex.isin(value,opt.depend)){
                            opt.depend.push(value)
                        }
                    })
                }
            })
            var final_list = ex.filter(ls,function(value){
                for(var i=0;i<self.has_depend_list.length;i++){
                    var depend_opt = self.has_depend_list[i]
                    if(depend_opt.value==value && depend_opt.depend.length>0){
                        return false
                    }
                }
                return true
            })


            this.update_disable()
            self.$refs.et.setCheckedKeys(final_list)
            self.row[self.head.name] = final_list

        },
        update_disable:function(){
            var self=this
            ex.each(this.has_depend_list,function(opt){
                if(opt.depend.length >0){
                    Vue.set(opt,'disabled',true)
                    //self.$refs.et.getCheckedKeys().
                    //opt.disableb=true
                }else{
                    Vue.set(opt,'disabled',false)
                }
            })
        },
        update_checked:function(node,valid_node_list){
            var self=this
            var depend_node_list=self.depend[node.value]
            if(depend_node_list){
                ex.each(depend_node_list,function(depend_node){
                    if(ex.isin(depend_node,valid_node_list) && self.is_depend_full_checked(depend_node)){
                        self.$refs.et.setChecked(depend_node.value,true,true)
                    }
                })
            }
            this.update_disable()
        },
        is_depend_full_checked:function(node){
            var ls =this.$refs.et.getCheckedKeys()
            if(node.depend){
                for(var i=0;i<node.depend.length;i++){
                    var depend_item = node.depend[i]
                    if(! ex.isin(depend_item,ls)){
                        return false
                    }
                }
            }
            return true
        },
        //filter_depend:function(ls){
        //    var out_list = ex.filter(ls,function(value){
        //        ex.each(this.depend_list,function(option)){
        //            if(option.value==value){
        //
        //            }
        //        }
        //    })
        //    return out_list
        //}
    },
    mounted:function(){
        var self=this
        self.depend={}
        self.has_depend_list=[]

        ex.walk(this.inn_head.options,function(opt){
            if(!opt.depend){
                return
            }
            self.has_depend_list.push(opt)
            ex.each(opt.depend,function(dep_value){
                if(! self.depend[dep_value]){
                    self.depend[dep_value]=[]
                }
                self.depend[dep_value].push(opt)
            })

        })
        var ls = self.row[self.head.name]
        for(var value in self.depend){
            if(ex.isin(value,ls)){
                var opt_list=self.depend[value]
                ex.each(opt_list,function(opt){
                    opt.depend.splice(opt.depend.indexOf(value),1)
                })
            }
        }

        this.update_disable()
    },
    data:function(){
        var inn_head=ex.copy(this.head)
        return {
            inn_head:inn_head,
            selected:[1,2],
            // demon 数据
            data: [{
                label: '一级 1',
                children: [{
                    label: '二级 1-1',
                    children: [{
                        label: '三级 1-1-1',
                        pk:1
                    }]
                }]
            }, {
                label: '一级 2',
                children: [{
                    label: '二级 2-1',
                    children: [{
                        label: '三级 2-1-1',
                        pk:3
                    }]
                }, {
                    label: '二级 2-2',
                    children: [{
                        label: '三级 2-2-1'
                    }]
                }]
            }, {
                label: '一级 3',
                children: [{
                    label: '二级 3-1',
                    children: [{
                        label: '三级 3-1-1',
                        pk:2
                    }]
                }, {
                    label: '二级 3-2',
                    children: [{
                        label: '三级 3-2-1'
                    }]
                }]
            }],
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
    ></el-tree>
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