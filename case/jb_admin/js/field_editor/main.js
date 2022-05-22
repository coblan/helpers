import * as invite_code from  './invite_code'
//import * as line_text from  './line_text'

import * as phone_code from  './phone_code'
import * as month from  './month'


import * as cascader from  './cascader'
// import * as field_date from  './date'
import * as pop_tree_select from  './pop_tree_select'
import * as compute from  './compute'

import * as range from  './range'
import * as time from  './time'
import * as list_ctn from  './list_ctn'

// import * as color from  './color'
//import * as number from  './number'
import * as richtext from  './richtext'
import * as split_text from  './split_text'


import int_field from './int.vue'
import  int_bool from  './int_bool.vue'

import  password from  './password.vue'
import  select from  './select.vue'
import search_select from  './search_select.vue'

import field_bool from  './bool.vue'
import  radio from  './radio.vue'

// import  flow from  './flow.vue'
// import  pop_table_multi_select from  './pop_table_multi_select.vue'

import  blocktext from  './blocktext.vue'
import  head_shower from  './head_shower.vue'
import  lineText from './lineText.vue'
// import  baseLine from './baseLine.vue'
import  number from './number.vue'
import singleCheckbox from "./singleCheckbox.vue";
// import pop_table_select from './pop_table_select.vue'
// import  inputOrUpload from './inputOrUpload.vue'
// import houreAndMinute from "./houreAndMinute.vue";
import guideHtml from "./guideHtml.vue";
// import minutePicker from "./minutePicker.vue";
// import ratioNumber from "./ratioNumber.vue";

Vue.component('com-field-blocktext',blocktext)
Vue.component('com-field-radio',radio)
Vue.component('com-field-int',int_field)
Vue.component('com-field-int-bool',int_bool)
Vue.component('com-field-password',password)
Vue.component('com-field-bool',field_bool)
Vue.component('com-field-select',select)

Vue.component('com-field-search-select',search_select)
// Vue.component('com-field-flow',flow)
// Vue.component('com-field-pop-table-multi-select',pop_table_multi_select)
Vue.component('com-field-head-shower',head_shower)

Vue.component('com-field-linetext',lineText)
// Vue.component('com-field-linetext',baseLine)

Vue.component('com-field-number',number)
Vue.component('com-field-single-checkbox',singleCheckbox)
// Vue.component('com-field-pop-table-select',pop_table_select)
// Vue.component('com-field-hour-and-minute',houreAndMinute)
// Vue.component('com-field-input-or-upload',inputOrUpload)
Vue.component('com-field-html-guide',guideHtml)
// Vue.component('com-field-minute',minutePicker)
// Vue.component('com-field-ratio-number',ratioNumber)
import jsonEdit from "./jsonEdit.vue";
Vue.component('com-field-json-edit',jsonEdit)

import lay_date from "./date.vue";
Vue.component('com-field-date',lay_date)

Vue.component('com-field-hour-and-minute', async (resolve, reject) =>{
    var com = await import(/* webpackChunkName: 'fields_import' */'./houreAndMinute.vue')
    resolve(com.default)
})
Vue.component('com-field-ratio-number', async (resolve, reject) =>{
    var com = await import(/* webpackChunkName: 'fields_import' */'./ratioNumber.vue')
    resolve(com.default)
})
Vue.component('com-field-minute', async (resolve, reject) =>{
    var com = await import(/* webpackChunkName: 'fields_import' */'./minutePicker.vue')
    resolve(com.default)
})
Vue.component('com-field-pop-table-select', async (resolve, reject) =>{
    var com = await import(/* webpackChunkName: 'fields_import' */'./pop_table_select.vue')
    resolve(com.default)
})
Vue.component('com-field-pop-table-select', async (resolve, reject) =>{
    var com = await import(/* webpackChunkName: 'fields_import' */'./pop_table_select.vue')
    resolve(com.default)
})
Vue.component('com-field-flow', async (resolve, reject) =>{
    var com = await import(/* webpackChunkName: 'fields_import' */'./flow.vue')
    resolve(com.default)
})
Vue.component('com-field-color', async (resolve, reject) =>{
    var com = await import(/* webpackChunkName: 'fields_import' */'./color.js')
    resolve(com.default)
})
Vue.component('com-field-pop-table-multi-select', async (resolve, reject) =>{
    var com = await import(/* webpackChunkName: 'fields_import' */'./pop_table_multi_select.vue')
    resolve(com.default)
})

Vue.component('com-field-input-or-upload', async (resolve, reject) =>{
    var com = await import(/* webpackChunkName: 'fields_import' */'./inputOrUpload.vue')
    resolve(com.default)
})
