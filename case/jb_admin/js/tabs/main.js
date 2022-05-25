// import * as tab_table from  './tab_table'
// import * as tab_fields from  './tab_fields'
import * as tab_fields_v1 from  './tab_fields_v1'  // 就是com-form-one
import * as tab_lazy_wrap from  './tab_lazy_wrap'
import * as tab_table_type from  './tab_table_type'
import * as tab_chart from  './tab_chart'


Vue.component('com-tab-dtable', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'fields_import' */'./tab_dtable.vue')
    resolve(com)
})


Vue.component('com-tab-table', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./tab_table.js')
    resolve(com)
})

Vue.component('com-tab-fields', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'not_use' */'./tab_fields.js')
    resolve(com)
})


