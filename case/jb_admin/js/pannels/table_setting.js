require('./styl/table_setting.styl')

Vue.component('com-panel-table-setting',{
    props:['ctx'],
    template:`<div class="com-panel-table-setting">
    <div class="head-panel">
         <el-checkbox-group v-model="advise_heads">
                <el-checkbox v-for="head in myheads" :label="head.name">
                    <span v-text="head.label"></span>
                </el-checkbox>
          </el-checkbox-group>
    </div>
    <div class="mybtn-panel">
         <el-button size="small" @click="clear_format()">恢复默认</el-button>
         <el-button type="primary" size="small" @click="make_catch()">确定</el-button>
    </div>

    </div>`,
    data(){
        return {
            advise_heads: this.ctx.table_ps.advise_heads
        }
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
            }else{
                var setting_obj ={
                    advise_heads:this.advise_heads,
                    advise_width:{}
                }
            }
            localStorage.setItem(key,JSON.stringify(setting_obj))

            this.$emit('finish')

        },
        clear_format(){
            var key = '_table_settings_'+ this.ctx.table_ps.director_name
            localStorage.clear(key)
            this.$emit('finish')
            location.reload()
        }
    }

})