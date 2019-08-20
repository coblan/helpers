require('./styl/table_setting.styl')

var table_setting_panel = {
    props:['ctx'],
    template:`<div class="com-panel-table-setting">
    <div class="head-panel">
        <div class="panel panel-info">
            <div class="panel-heading">普通列</div>
            <div style="padding: 10px">
             <el-checkbox-group class="mygroup" v-model="heads_bucket._first_layer">
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
                  <el-checkbox-group class="mygroup" v-model="heads_bucket[field_group.name]">
                    <el-checkbox v-for="head in field_list(field_group.children)" :data-id="head.name" :label="head.name" size="small" border>
                            <span v-text="head.label"></span>
                    </el-checkbox>
                  </el-checkbox-group>
             </div>

        </div>

    </div>


    <div class="mybtn-panel">
         <el-button size="small" @click="clear_format()">恢复默认</el-button>
         <el-button type="primary" size="small" @click="make_catch()">确定</el-button>
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
            order_bucket:[],
            first_layer_field:first_layer_field,
            group_field_list:group_field_list,
        }
    },
    mounted(){
        var self = this
        var ddom= $(this.$el).find('.mygroup')
       ex.each(ddom,function(mydom){
           var order_list =[]
           self.order_bucket.push(order_list)
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
        make_catch(){
            this.advise_heads = []
            this.advise_order = []
            for(var key in this.heads_bucket){
                var mylist = this.heads_bucket[key]
                this.advise_heads = this.advise_heads.concat(mylist)
            }
            ex.each(this.order_bucket,(mylist)=>{
                this.advise_order = this.advise_order.concat(mylist)
            })

            this.ctx.table_ps.advise_heads = this.advise_heads
            this.ctx.table_ps.advise_order = this.advise_order
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
                this.ctx.table_ps.heads = []
                setTimeout(()=>{
                    this.ctx.table_ps.heads =tmp
                    this.ctx.table_ps.$emit('data-updated-backend')
                },200)
            }
            this.$emit('finish')
        },
        clear_format(){
            var key = '_table_settings_'+ this.ctx.table_ps.director_name
            localStorage.clear(key)
            this.$emit('finish')
            cfg.show_load()
            location.reload()
        }
    }
}

Vue.component('com-panel-table-setting',function(resolve,reject){
    ex.load_js_list([js_config.js_lib.sortablejs,'https://cdnjs.cloudflare.com/ajax/libs/Vue.Draggable/2.20.0/vuedraggable.umd.min.js'],()=>{
        resolve(table_setting_panel)
    })
})

