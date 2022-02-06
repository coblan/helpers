import * as table from  './table'
import * as table_type from  './table_type'
import * as fields from  './fields'
import * as table_grid from  './table_grid'
import * as live_table_chart from  './table_chart.vue'
import tab from  './tab.vue'
import myhtml from './html.vue'
import lazyWrap  from "./lazyWrap.vue";
Vue.component('com-table-chart',function(resolve,reject){
    ex.load_js(js_config.js_lib.echarts).then(function(){
        resolve(live_table_chart)
    })
})
Vue.component('com-live-tab',tab)
Vue.component('com-live-html',myhtml)
Vue.component('com-lazy-wrap',lazyWrap)