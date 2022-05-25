
require('./scss/fields.scss')
require('./table_editor/scss/table_editor_base.scss')
require('./scss/tab.scss')
require('./scss/table.scss')
require('./scss/table_page.scss')
require('./scss/element_ex.scss')
require('./scss/share.scss')
require('./scss/layer.scss')
require('./scss/my_bootstrap.scss')

require('./styl/adminlte.styl')
require('weblib/pc/style/element_ex.scss')
import  'weblib/pc/style'


import  director_table from  './pannels/director_table.vue'
import  backendTable from './pannels/backendTable.vue'
import d_table_setting from 'webcase/director/table/dsetting.vue'
import excelProcessResult from "./misc/excelProcessResult.vue";
import livepage_tab from  './livepage/tab.vue'
import  live_table_chart from  './livepage/table_chart.vue'
// import tab_dtable from './tabs/tab_dtable.vue'
import  formOne from './misc/formOne.vue'
export {
    director_table,
    backendTable,
    d_table_setting,
    excelProcessResult,

    livepage_tab,
    live_table_chart,
    // tab_dtable,
    formOne
}
// Vue.component('com-d-table',director_table_1)