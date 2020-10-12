import * as form_one from  './form_one'
import login_head from  './login_head.vue'
import login_footer from  './login_footer.vue'
import el_button from  './el_button.vue'
import el_drop_btn from  './el_drop_btn.vue'
import  vertical_layout from  './vertical_layout.vue'

Vue.component('com-ui-login-head',login_head)
Vue.component('com-ui-login-footer',login_footer)
Vue.component('com-btn',el_button)
Vue.component('com-btn-drop',el_drop_btn)
Vue.component('com-layout-vertical',vertical_layout)