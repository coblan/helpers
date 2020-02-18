
require('./styl/live.styl')

import * as live_list from './live_list.js'
import * as live_fields from './live_fields.js'
import * as live_list_page from './live_list_page.js'
import * as live_layout from './live_layout.js'
import * as live_swip_tab from './live_swip_tab.js'

import  live_login from './live_login.vue'
import  live_cell from './live_cell.vue'
import  live_info from './live_info.vue'
window.live_login = live_login
window.live_cell = live_cell
window.live_info = live_info
//Vue.component('com-live-login',live_login)