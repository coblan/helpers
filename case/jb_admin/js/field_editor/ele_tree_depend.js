require('./scss/ele_tree_name_layer.scss')

export default  {
    props:['row','head'],

    methods:{
        check_depend:function(node){
            var self=this
            if(node.depend_list){
                ex.each(node.depend_list,function(dep_node){
                    var node = self.$refs.et.getNode(dep_node.value)
                    if(node && !node.checked){
                        self.$refs.et.setChecked(dep_node.value,true)
                        self.check_depend(dep_node)
                    }
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
                    var node = self.$refs.et.getNode(dep_node.value)
                    if(node && node.checked){
                        self.$refs.et.setChecked(dep_node.value,false)
                        self.uncheck_depended(dep_node)
                    }
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
            var namelist =[]
            ex.walk(this.inn_head.options,(option)=>{
                if(option.value){
                    namelist.push(option.value)
                }
            })
            if(this.row[this.head.name] && this.row[this.head.name].length >0){
                this.row[this.head.name] = ex.filter(this.row[this.head.name],(item)=>{return ! ex.isin(item,namelist)})
                this.row[this.head.name] = this.row[this.head.name].concat( ls )
            }else{
                this.row[this.head.name] = ls
            }
        },
        filterNode(value, data) {
            if (!value) return true;
            return data.label.indexOf(value) !== -1;
        },
        init(){
            var self=this
            self.depend={}
            self.has_depend_list=[]

            var options_dict ={}
            ex.walk(this.inn_head.options,function(opt){
                if(opt.value){
                    if(options_dict[opt.value]){
                        cfg.showError(opt.value +'重复了，请检查备选项！')
                    }
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
                    if(!item){
                        cfg.showError(`${item_name}不存在，而被 ${opt.label} 依赖!`)
                    }
                    opt.depend_list.push(item)
                    if(!item.depended_list){
                        item.depended_list = []
                    }
                    item.depended_list.push(opt)
                })
            })
        },
        refresh(options){
            this.inn_head.options =[]
            setTimeout(()=>{
                this.inn_head.options= options
                this.init()
            },300)
        }
    },
    mounted:function(){
        this.init()
        ex.vueEventRout(this)
    },
    watch: {
        filterText(val) {
            this.$refs.et.filter(val);
        },
    },
    data:function(){
        var inn_head=ex.copy(this.head)
        return {
            parStore:ex.vueParStore(this),
            filterText:'',
            inn_head:inn_head,
            defaultProps: {
                children: 'children',
                label: 'label',
            }
        }
    },
    template:`<div class="com-field-ele-tree-name-layer">
    <el-input
      placeholder="输入关键字进行过滤"
      v-model="filterText">
    </el-input>
        <el-tree ref="et" :data="inn_head.options" :props="defaultProps"
             @node-click="handleNodeClick"
             @check="handleCheck"
             show-checkbox
             @check-change="handleCheckChange"
             :default-checked-keys="row[head.name]"
             node-key="value"
             :filter-node-method="filterNode"
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

// Vue.component('com-field-ele-tree-depend',label_shower)

//Vue.component('com-field-ele-tree-name-layer',function(resolve,reject){
//ex.load_css('https://unpkg.com/element-ui/lib/theme-chalk/index.css')
//ex.load_js('https://unpkg.com/element-ui/lib/index.js',function(){
//resolve(label_shower)
//})
//})