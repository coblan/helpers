
import './scss'
import * as config from  './config.js'

//table mix
import * as mix_table_data from  './mix/mix_table_data.js'
// import * as mix_v_table_adapter from './mix/mix_v_table_adapter.js'

import * as mix_ele_table_adapter from './mix/mix_ele_table_adapter.js'
import * as mix_main from './mix/main'

// import * as ajax_fields from './tabs/ajax_fields.js'
// import * as ajax_table from './tabs/ajax_table.js'
//import * as com_pop_fields from './com_pop_fields.js'

import * as ele_tree from  './field_editor/ele_tree.js'


// table editor
// import * as table_picture from  './table_editor/picture.js'
import * as table_label_shower from  './table_editor/label_shower.js'
import * as table_mapper from  './table_editor/mapper.js'
import * as call_fun from  './table_editor/call_fun.js'
import * as table_pop_fields from  './table_editor/pop_fields.js'
import * as pop_fields_local from  './table_editor/pop_fields_local.js'
import * as table_linetext from  './table_editor/linetext.js'
import * as table_checkbox from  './table_editor/check_box.js'
import * as switch_to_tab from  './table_editor/switch_to_tab.js'
import * as select from  './table_editor/select.js'
import * as extra_click from  './table_editor/extra_click.js'
import * as extra_click_plus from  './table_editor/extra_click_plus.js'
import * as array_mapper from  './table_editor/array_mapper.js'

import * as bool_shower from  './table_editor/bool_shower.js'
import * as foreign_click_select from  './table_editor/foreign_click_select.js'
import * as array_option_mapper from  './table_editor/array_option_mapper.js'
import * as html_shower from  './table_editor/html_shower.js'
import * as bool_editor from  './table_editor/bool_editor.js'
import * as jump_link from  './table_editor/jump_link.js'
import * as change_order from  './table_editor/change_order.js'
import * as digit from  './table_editor/digit.js'
import * as append_html_shower from  './table_editor/append_html_shower.js'
import * as array_obj_shower from  './table_editor/array_obj_shower.js'
import * as pop_table from  './table_editor/pop_table.js'

import * as table_type_main from  './table_type_editor/main.js'



// table operator
import * as op_a from  './table_operator/operator_a.js'
import * as delete_op from  './table_operator/delete_op.js'
import * as operator_btn from  './table_operator/operator_btn.js'

//fields operator
import * as btn from  './field_operator/btn.js'

//import * as validate from  './validator'

//import * as com_table from  './misc/com_table.js'

//misc
import * as pop_table_layer from  './misc/pop_table_layer.js'
import * as pop_fields_layer from  './misc/pop_fields_layer.js'
import * as pop_layer from  './misc/pop_layer'
import * as misc_main from  './misc/main.js'


// import * as ele_table from  './table_panels/ele_table.js'



// top_heads
// element的下拉header 应该是无用的。
// import * as dropdown from  './header/dropdown.js'
import * as sm_link from  './header/sm_link.js'
import * as header_main from  './header/main.js'

//ui
// import * as stack_widget from './misc/stack_widget'
// store
//import * as table_store from './store/table_store'


import * as table_editor_main from  './table_editor/main.js'




import * as node_store_main from  './node_store/main.js'
import * as tabs_main from  './tabs/main'

import * as operator_main from  './operator/main.js'
import * as filter_editor_main from  './filter_editor/main.js'
import * as livepage_main from  './livepage/main.js'
import * as table_operator_main from  './table_operator/main'

import * as table_filter_main from './table_filter/main'

import * as page_com_main from './page_com/main'
import  * as table_local_input from './table_editor/local_input/main'

// import * as layout_main from './layout'
//import * as pop_win_main from './pop_win/main'



// import(/* webpackChunkName: 'table_group' */'./table_group/main.js')
// import(/* webpackChunkName: 'fields_main' */'./fields_main.js')

import * as fields_main from  './fields_main.js'

//这里面的东西好像都过时了，现在用的com-d-table  发现有用的： com-table-filters
// import * as table_group_main from  './table_group/main.js'
// import * as filter from  './table_group/filter.js'

import  * as table_group from './table_group.js'
import * as table_filter from './filter_main.js'
import * as maybe_old from './maybe_old.js'


import componentPannel from "./pannels/componentPannel.vue";
Vue.component('com-component-pannel',componentPannel)