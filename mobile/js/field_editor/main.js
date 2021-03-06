require('./styl/main.styl')

import * as index_select from './index_select.js'
import * as linetext from './linetext.js'
import * as password from './password.js'
import * as blocktext from './blocktext.js'
import * as phone from './phone.js'
import * as select from './select.js'
import * as picture from './picture.js'
import * as multi_picture from './multi_picture.js'
import * as phone_code from './phone_code.js'
//import * as field_number from './field_numberber.js'
import * as label_shower from './label_shower.js'
import * as bool from './bool.js'
import * as date from './date.js'
import * as datetime from './datetime.js'
import * as tree_select from './tree_select.js'

import * as pop_table_select from './pop_table_select.js'

import  validate_code from './validate_code.vue'
import  switch_btn from './switch.vue'

import  field_number from './field_number.vue'
import  field_int from './int.vue'
import  banner from './banner.vue'
Vue.component('com-field-number',field_number)
Vue.component('com-field-int',field_int)
Vue.component('com-field-validate-code',validate_code)
Vue.component('com-field-switch',switch_btn)
Vue.component('com-field-banner',banner)