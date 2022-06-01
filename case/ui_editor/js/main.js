import editorTab from "./ui_editor/editorTab.vue";
//
Vue.component('com-tab-ui-editor',editorTab)

import test from './ui_editor/test.vue'
Vue.component('com-ui-test',test)

cfg.ui_editor.test = editorTab


import mountView from './coms/mountView.vue'
import backendTable from './coms/backendTable.vue'

Vue.component('uie-mount-view',mountView)
Vue.component('uie-backendTable',backendTable)