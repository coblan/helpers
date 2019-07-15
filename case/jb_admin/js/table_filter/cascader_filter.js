var cascasder_filter = {
    props:['head','search_args'],

    template:`<div class="com-filter-cascasder">
       <el-cascader
            :show-all-levels="false"
            v-model="search_args[head.name]"
            :options="head.options"
            :props="{checkStrictly: true ,emitPath:false}"
            size="small"
            clearable>
        </el-cascader>
    </div> `,

}
Vue.component('com-filter-cascasder',cascasder_filter)