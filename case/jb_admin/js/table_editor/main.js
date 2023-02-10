import * as pop_fields_from_row from  './pop_fields_from_row.js'
import * as sequence from  './sequence.js'
import * as style_block from  './style_block.js'
import * as ops_cell from  './ops_cell.js'
// import * as table_span from  './span.js'
import * as array_shower from  './array_shower.js'
// import * as click from  './click.js'
import * as my_json from  './json.js'
import * as multi_image from  './multi_image.js'
import * as map_html from  './map_html.js'
import * as link from  './link.js'
import * as rich_span from  './rich_span.js'
import * as multi_row from  './multi_row.js'
import * as color from  './color.js'
import * as icon_cell from  './icon_cell.js'
import hourAndMinute  from "./hourAndMinute.vue";
import  com_tag from './tag_map.vue'
import buttonClick  from "./buttonClick.vue";
import tableSpan from './tableSpan.vue'
import ratioNumber from "./ratioNumber.vue";
import onlytext from "./onlytext.vue";
import qrcode from "./qrcode.vue";
Vue.component('com-table-tag-map',com_tag)
Vue.component('com-table-button-click',buttonClick)
Vue.component('com-table-hour-and-minute',hourAndMinute)
Vue.component('com-table-span',tableSpan)
Vue.component('com-table-ratio-number',ratioNumber)
Vue.component('com-table-onlytext',onlytext)
Vue.component('com-table-qrcode',qrcode)
import click from './click.vue'
Vue.component('com-table-click',click)
import  treeFirst from './treeFirst.vue'
Vue.component('com-table-tree-first',treeFirst)
import tablePre  from "./tablePre.vue";
Vue.component('com-table-pre',tablePre)
import * as table_input_main from './table_input/main'

/*

按钮组
================
{'name':'extra_op',
     'label':'操作',
     'editor':'com-table-ops-cell',
     'ops':[
     {
     'editor':'com-op-plain-btn',
     'label':'详情',
     'class':'btn btn-primary btn-xs',
     'action':"""rt=scope.ps.switch_to_tab({
     par_row:scope.row,
     tab_name: 'baseinfo',
     ctx_name: 'detail_tabs', })"""}
     ],
 }

*
*
* */