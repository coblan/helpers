var multi_level_select={
    props:['row','head'],
    template:`<div class="com-field-multi-level-select">
            <el-cascader
              :options="head.options"
              v-model="row[head.name]"></el-cascader>
               </div>`,
    mounted:function(){

    },
    data:function(){
        return {
            //options:china_address
        }
    }
}
Vue.component('com-field-multi-level-select',multi_level_select)
