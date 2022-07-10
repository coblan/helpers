import editorTab from "./ui_editor/editorTab.vue";
//
Vue.component('com-tab-ui-editor',editorTab)

import test from './ui_editor/test.vue'
Vue.component('uie-test',test)




import mountView from './coms/mountView.vue'
import backendTable from './coms/backendTable.vue'
import generalWrap from "./coms/generalWrap.vue";
Vue.component('uie-mount-view',mountView)
Vue.component('uie-backendTable',backendTable)
Vue.component('uie-general-wrap',generalWrap)

import './coms'