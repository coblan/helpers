import * as sys_link from  './sys_link.js'
import * as user_info from  './user_info.js'
import * as space from  './space.js'
// import * as bell_msg from  './bell_msg.js'
import bellMessage from './bellMessage.vue'
Vue.component('com-head-bell-msg',bellMessage)

import historyPage from './historyPage.vue'
Vue.component('com-historypage',historyPage)

import datetime from './datetime.vue'
Vue.component('com-head-datetime',datetime)
import pageLink from "./pageLink.vue";
Vue.component('com-head-page-link',pageLink)
import dropMenu from './dropMenu.vue'
Vue.component('com-head-dropmenu',dropMenu)