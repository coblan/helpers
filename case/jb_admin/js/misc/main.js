
// import form_one from './formOne.vue'
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
// Vue.component('com-form-one',form_one)

import stack_widget from './stack_widget.vue'
Vue.component('com-widget-stack',stack_widget)
window.live_el_tab = el_tab