// field editor
import * as fields_editor_main from  './field_editor/main.js'
import * as field_label_shower from  './field_editor/label_shower.js'
import * as ele_transfer from  './field_editor/ele_transfer.js'
import * as datetime from  './field_editor/datetime.js'
// import * as pop_table_select from  './field_editor/pop_table_select.js'
import * as plain_file from  './field_editor/plain_file.js'
import * as validate_code from  './field_editor/validate_code.js'
import * as order_list_table from  './field_editor/order_list_table.js'
//import * as phon_code from  './field_editor/phon_code.js'
import * as ele_tree_depend from  './field_editor/ele_tree_depend.js'
import * as com_china_address from  './field_editor/china_address.js'

//fields_panels
import * as panels_main from  './pannels/main.js'
import * as sim_fields from  './fields_panels/sim_fields.js'
import * as sim_fields_local from  './fields_panels/sim_fields_local.js'

import * as pop_edit_local from  './fields_panels/pop_edit_local.js'
import * as plain_field_panel from  './fields_panels/plain_field_panel.js'

import * as nice_validator_rule from  './nice_validator_rule.js'
import * as fields_panels_main from  './fields_panels/main.js'


Vue.component('com-d-table', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'fields_import' */'./fields_import.js')
    resolve(com.director_table)
})
Vue.component('com-backend-table', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'fields_import' */'./fields_import.js')
    resolve(com.backendTable)
})
Vue.component('com-d-table-setting', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'fields_import' */'./fields_import.js')
    resolve(com.d_table_setting)
})
Vue.component('com-excel-process-result', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'fields_import' */'./fields_import.js')
    resolve(com.excelProcessResult)
})

Vue.component('com-live-tab', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'fields_import' */'./fields_import.js')
    resolve(com.livepage_tab)
})

Vue.component('com-table-chart',async(resolve,reject) =>{
    var com = await import(/* webpackChunkName: 'fields_import' */'./fields_import.js')
    await ex.load_js(js_config.js_lib.echarts)
    resolve(com.live_table_chart)

    // ex.load_js(js_config.js_lib.echarts).then(function(){
    //     resolve(com.live_table_chart)
    // })
})
Vue.component('com-tab-dtable', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'fields_import' */'./fields_import.js')
    resolve(com.tab_dtable)
})

Vue.component('com-form-one', async (resolve, reject) =>{
    var com = await import(/* webpackChunkName: 'fields_import' */'./fields_import.js')
    resolve(com.formOne)
})


