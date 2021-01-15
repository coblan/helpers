
require('./styl/live.styl')

import * as live_list from './live_list.js'
import * as live_fields from './live_fields.js'
import * as live_list_page from './live_list_page.js'
import * as live_layout from './live_layout.js'
import * as live_swip_tab from './live_swip_tab.js'

import  live_login from './live_login.vue'
import  live_cell from './live_cell.vue'
import  live_info from './live_info.vue'
import  live_html from './live_html.vue'
import  live_search from './live_search.vue'
import  live_search_list from './live_search_list.vue'
import  live_page from './live_page.vue'

window.live_login = live_login
window.live_cell = live_cell
window.live_info = live_info
window.live_html = live_html
window.live_search = live_search
window.live_search_list = live_search_list
window.live_page = live_page

//Vue.component('com-live-login',live_login)