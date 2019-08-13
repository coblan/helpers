require('./styl/table_setting.styl')

var table_setting_panel = {
    props:['ctx'],
    template:`<div class="com-panel-table-setting">

    <div class="head-panel">
         <el-checkbox-group class="mygroup" v-model="advise_heads">
                <el-checkbox v-for="head in myheads" :data-id="head.name" :label="head.name">
                    <span v-text="head.label"></span>
                </el-checkbox>
          </el-checkbox-group>
    </div>

    <!--<div class="head-panel">-->
        <!--<draggable v-model="advise_heads" group="people" @start="drag=true" @end="drag=false">-->
            <!--<el-checkbox v-for="head in myheads" :label="head.name">-->
                        <!--<span v-text="head.label"></span>-->
            <!--</el-checkbox>-->
        <!--</draggable >-->

    <!--</div>-->

    <div class="mybtn-panel">
         <el-button size="small" @click="clear_format()">恢复默认</el-button>
         <el-button type="primary" size="small" @click="make_catch()">确定</el-button>
    </div>

    </div>`,
    data(){
        return {
            advise_heads: this.ctx.table_ps.advise_heads,
            advise_order: []
        }
    },
    mounted(){
        var ddom= $(this.$el).find('.mygroup')[0]
        var self = this
         new Sortable(ddom ,{
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
                     self.advise_order = sortable.toArray()
                 }
             }
         } )
    },
    computed:{
        myheads(){
            return ex.filter(this.ctx.table_ps.heads,(head)=>{
                return head.name
            })
        }
    },
    methods:{
        make_catch(){
            this.ctx.table_ps.advise_heads = this.advise_heads

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

            //var key = '_table_settings_'+ self.ctx.table_ps.director_name
            //var setting_str = localStorage.getItem(key)
            //if(setting_str){
            //    var setting_obj = JSON.parse(setting_str)
            //    setting_obj.advise_order = sortable.toArray()
            //    self.ctx.table_ps.heads = ex.sort_by_names(self.ctx.table_ps.heads,setting_obj.advise_order,true)
            //    localStorage.setItem(key,JSON.stringify(setting_obj))
            //}

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
            location.reload()
        }
    }
}

Vue.component('com-panel-table-setting',function(resolve,reject){
    ex.load_js_list([js_config.js_lib.sortablejs,'https://cdnjs.cloudflare.com/ajax/libs/Vue.Draggable/2.20.0/vuedraggable.umd.min.js'],()=>{
        resolve(table_setting_panel)
    })
})

