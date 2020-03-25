require('./styl/multi_select.styl')

var multi_select = {
    props:['head','search_args'],

    template:`<div class="com-filter-multi-select" :style="{width:head.width}">
       <!--<el-cascader-->
            <!--:show-all-levels="false"-->
            <!--v-model="search_args[head.name]"-->
            <!--:options="head.options"-->
            <!--:props="{checkStrictly: true ,emitPath:false}"-->
            <!--size="small"-->
            <!--clearable>-->
        <!--</el-cascader>-->
 <!--<option v-for='option in orderBy(options,"label")' :value="option.value" v-text='option.label'></option>-->
    <span  class="title-span" v-if="head.show_label"><span  v-text="head.label"></span>:</span>
       <el-select
            v-model="search_args[head.name]"
            multiple
            collapse-tags
            style="margin-left: 20px;"
            size="small"
            placeholder="请选择">
            <el-option
            disabled
            :label="head.label"
            :value="undefined"
            >
            </el-option>
            <el-option
              v-for="option in options"
              :key="option.value"
              :label="option.label"
              :value="option.value">
            </el-option>
       </el-select>
    </div> `,
    computed:{
        options:function(){
            if(this.head.ctx_name){
                return named_ctx[this.head.ctx_name]
            }else{
                return this.head.options
            }
        }
    },

}
Vue.component('com-filter-multi-select',multi_select)