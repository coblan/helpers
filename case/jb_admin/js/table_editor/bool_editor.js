
var bool_shower = {
    props:['rowData','field','index'],
    template:`<span>
       <el-switch
              v-model="is_true"
              active-color="#13ce66"
              inactive-color="#ff4949">
        </el-switch>
    </span>`,

    computed:{
        is_true: {
            get: function () {
                var value = this.rowData[this.field]
                if(value == 1) {
                    return true
                }else{
                    return value
                }
            },
            set: function (newValue) {
                var crt_value = this.rowData[this.field]
                if(crt_value == 0 || crt_value == 1) {
                    this.rowData[this.field] = newValue ? 1 : 0
                }else{
                    this.rowData[this.field] = newValue
                }
            }
        },
    }

}

Vue.component('com-table-bool-editor',bool_shower)
