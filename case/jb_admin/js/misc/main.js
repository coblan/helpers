import * as form_one from  './form_one'
import login_head from  './login_head.vue'
import login_footer from  './login_footer.vue'
import el_button from  './el_button.vue'
import el_drop_btn from  './el_drop_btn.vue'
import  vertical_layout from  './vertical_layout.vue'
import  el_tab from './el_tab_widget.vue'
import  line_info from  './line_info.vue'
import messageInfo from "./messageInfo.vue";
Vue.component('com-ui-login-head',login_head)
Vue.component('com-ui-login-footer',login_footer)
Vue.component('com-btn',el_button)
Vue.component('com-btn-drop',el_drop_btn)
Vue.component('com-layout-vertical',vertical_layout)
Vue.component('com-line-info',line_info)

Vue.component('com-widget-el-tab',el_tab)
Vue.component('com-message-rows',messageInfo)
window.live_el_tab = el_tab