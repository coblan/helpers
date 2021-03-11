import  pannel_main from './panel'
import * as table_chart_editor_main from './table_chart_editor/main'

import tab_table_chart from './tab/tab_table_chart.vue'
import  chart_general from  './charts/general.vue'
import  horizen_type_bar from  './charts/horizen_type_bar.vue'
import  category_bar from  './charts/category_bar.vue'
import  pie from  './charts/pie.vue'

Vue.component('com-chart-general',chart_general)
Vue.component('com-chart-horizen-type-bar',horizen_type_bar)
Vue.component('com-chart-category-bar',category_bar)
Vue.component('com-chart-pie',pie)

Vue.component('com-tab-table-chart',tab_table_chart)

