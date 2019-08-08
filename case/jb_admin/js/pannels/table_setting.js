Vue.component('com-panel-table-setting',{
    props:['ctx'],
    template:`<div class="com-panel-table-setting">
        <el-checkbox-group v-model="approve_heads">
            <el-checkbox v-for="head in myheads" :label="head.label" :true-label="head.name"></el-checkbox>
      </el-checkbox-group>
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