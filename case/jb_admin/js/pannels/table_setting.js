require('./styl/table_setting.styl')

Vue.component('com-panel-table-setting',{
    props:['ctx'],
    template:`<div class="com-panel-table-setting">
    <div class="head-panel">
         <el-checkbox-group v-model="approve_heads">
                <el-checkbox v-for="head in myheads" :label="head.name">
                    <span v-text="head.label"></span>
                </el-checkbox>
          </el-checkbox-group>
    </div>
    <div class="mybtn-panel">
         <el-button size="small">清除格式</el-button>
         <el-button type="primary" size="small">确定</el-button>
    </div>

    </div>`,
    data(){
        return {
            approve_heads: []
        }
    },
    computed:{
        myheads(){
            return ex.filter(this.ctx.table_ps.heads,(head)=>{
                return head.name
            })
        }
    }

})