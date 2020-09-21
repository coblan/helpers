require('./styl/table_setting.styl')

var table_setting_panel = {
    props:['ctx'],
    template:`<div class="com-panel-table-setting">
    <div class="head-panel">
        <div class="panel panel-info">
            <div class="panel-heading">普通列</div>
            <div style="padding: 10px">
             <el-checkbox-group class="mygroup" v-model="heads_bucket._first_layer" data-name="_first_layer">
                <el-checkbox v-for="head in first_layer_field" :data-id="head.name" :label="head.name" size="small" border>
                    <i class="fa fa-level-down" aria-hidden="true" v-if="head.children"></i>
                        <span v-text="head.label"></span>
                </el-checkbox>
             </el-checkbox-group>
            </div>

        </div>

        <div class="panel panel-warning" v-for="field_group in group_field_list">
             <div class="panel-heading"> <span v-text="field_group.label"></span></div>
             <div style="padding: 10px">
                  <el-checkbox-group class="mygroup" v-model="heads_bucket[field_group.name]" :data-name="field_group.name">
                    <el-checkbox v-for="head in field_list(field_group.children)" :data-id="head.name" :label="head.name" size="small" border>
                            <span v-text="head.label"></span>
                    </el-checkbox>
                  </el-checkbox-group>
             </div>

        </div>

    </div>


    <div class="mybtn-panel">
         <el-button size="small" @click="clear_format()">恢复默认</el-button>
         <el-button type="primary" size="small" @click="change_advise_heads()">确定</el-button>
    </div>

    </div>`,
    data(){
        var  advise_heads = this.ctx.table_ps.advise_heads
        var  advise_order = this.ctx.table_ps. advise_order
        var table_heads = ex.sort_by_names(this.ctx.table_ps.heads,advise_order,true)
        var first_layer_field =ex.filter(table_heads,(head)=>{
                return ! head.sublevel
            })
        var group_field_list =ex.filter(table_heads,(head)=>{
                return head.children
            })

        var first_layer_heads_name = ex.map(first_layer_field,(head)=>{
            return head.name
        })
        var first_layer_advise_heads = ex.filter(advise_heads,(name)=>{
            return ex.isin(name,first_layer_heads_name)
        })
        var heads_bucket ={
            _first_layer:first_layer_advise_heads,
        }
        ex.each(group_field_list,(group_head)=>{
            heads_bucket[group_head.name]= ex.filter(advise_heads,(name)=>{
                return ex.isin(name,group_head.children)
            })
        })

        return {
            table_heads:table_heads,
            advise_heads: advise_heads,
            advise_order: advise_order,
            heads_bucket:heads_bucket,
            order_bucket:{},
            first_layer_field:first_layer_field,
            group_field_list:group_field_list,
        }
    },
    mounted(){
        var self = this
        var ddom= $(this.$el).find('.mygroup')
       ex.each(ddom,function(mydom){
           var name = $(mydom).attr('data-name')
           var order_list =[]
           self.order_bucket[name] = order_list
            new Sortable(mydom ,{
                animation: 150,
                store: {
                    /**
                     * Get the order of elements. Called once during initialization.
                     * @param   {Sortable}  sortable
                     * @returns {Array}
                     */
                    //get: function (sortable) {
                    //    var order = localStorage.getItem(sortable.options.group.name);
                    //    return order ? order.split('|') : [];
                    //},

                    /**
                     * Save the order of elements. Called onEnd (when the item is dropped).
                     * @param {Sortable}  sortable
                     */
                    set: function (sortable) {
                        //self.advise_order = sortable.toArray()
                        order_list.splice(0,order_list.length,...sortable.toArray())
                    }
                }
            } )

        })


    },
    computed:{
        myheads(){
            return ex.filter(this.ctx.table_ps.heads,(head)=>{
                return head.name
            })
        },

    },
    methods:{
        field_list(children){
            return ex.filter(this.table_heads,(head)=>{
                return  ex.isin(head.name,children)
            })
        },
        change_advise_heads(){
            this.advise_heads = []
            this.advise_order = []
            for(var key in this.heads_bucket){
                var mylist = this.heads_bucket[key]
                this.advise_heads = this.advise_heads.concat(mylist)
            }
            this.advise_order = this.order_bucket._first_layer
            ex.each(this.group_field_list,(head)=>{
                var index = this.advise_order.indexOf(head.name)
                var mylist = this.order_bucket[head.name]
                this.advise_order.splice(index,0,...mylist)
            })

            //ex.each(this.order_bucket,(mylist)=>{
            //
            //    this.advise_order = this.advise_order.concat(mylist)
            //})

            // [1]如果 增加了 不存在的 head，必须重新获取数据
            for(var i=0;i<this.advise_heads.length;i++){
                var head_name = this.advise_heads[i]
                if(!ex.isin(head_name,this.ctx.table_ps.advise_heads)){
                    setTimeout(()=>{
                        this.ctx.table_ps.search()
                    },50)
                    this.set_cookie_advise_heads()
                    break
                }
            }
            // advise_heads发生变换时，可能需要设置cookie (如果新老heads有交叉的情况，上面[1]会触发search解决这个问题)
            if(this.advise_heads.length != this.ctx.table_ps.advise_heads.length){
                this.set_cookie_advise_heads()
            }

            this.ctx.table_ps.advise_heads = this.advise_heads
            if(this.advise_order.length >0){
                this.ctx.table_ps.advise_order = this.advise_order
            }

            var key = '_table_settings_'+ this.ctx.table_ps.director_name
            var setting_str = localStorage.getItem(key)
            if(setting_str){
                var setting_obj = JSON.parse(setting_str)
                setting_obj.advise_heads = this.advise_heads
                if(this.advise_order.length >0){
                    setting_obj.advise_order = this.advise_order
                }

            }else{
                var setting_obj ={
                    advise_heads:this.advise_heads,
                    advise_width:{},
                    advise_order:this.advise_order,
                }
            }

            localStorage.setItem(key,JSON.stringify(setting_obj))

            if(this.advise_order.length >0){
                var tmp =ex.sort_by_names(this.ctx.table_ps.heads,this.advise_order,true)
                var tmp_rows = this.ctx.table_ps.rows

                this.ctx.table_ps.heads = []
                this.ctx.table_ps.rows=[]

                setTimeout(()=>{
                    this.ctx.table_ps.heads =tmp
                    this.ctx.table_ps.rows= tmp_rows
                    this.ctx.table_ps.$emit('data-updated-backend')
                },200)
            }
            this.$emit('finish')
        },
        clear_format(){
            var key = '_table_settings_'+ this.ctx.table_ps.director_name
            localStorage.clear(key)
            this.clear_cookie_advise_heads()

            this.$emit('finish')
            cfg.show_load()
            location.reload()
        },
        set_cookie_advise_heads(){
            var advise_heads_str=this.advise_heads.join(',')
            if(this.ctx.table_ps.advise_heads_cookie_path){
                var cookie_str=`advise_heads=${advise_heads_str};path=${this.ctx.table_ps.advise_heads_cookie_path}`
                document.cookie = cookie_str
            }
        },
        clear_cookie_advise_heads(){
            if(this.ctx.table_ps.advise_heads_cookie_path){
                var cookie_str=`advise_heads=;path=${this.ctx.table_ps.advise_heads_cookie_path};Max-Age=0`
                document.cookie = cookie_str
            }
        }
    }
}

Vue.component('com-panel-table-setting',function(resolve,reject){
    ex.load_js_list([js_config.js_lib.sortablejs,'https://cdnjs.cloudflare.com/ajax/libs/Vue.Draggable/2.20.0/vuedraggable.umd.min.js'],()=>{
        resolve(table_setting_panel)
    })
})

