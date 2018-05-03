require('./scss/check_box.scss')
import {mix_editor} from  './mix_editor.js'
var check_box = {
    props:['rowData','field','index'],
    template:`<div :class="['com-table-checkbox',{'dirty':is_dirty}]"><input style="width: 100%" @change="on_changed()" type="checkbox" v-model="rowData[field]"></div>`,
    mixins:[mix_editor]
}

Vue.component('com-table-checkbox',check_box)
