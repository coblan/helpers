import {pop_table} from "./table_editor/pop_table";


Vue.component('com-table-panel', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./pannels/table_panel.js')
    resolve(com.default)
})

Vue.component('com-panel-pop-fields', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./pannels/pop_fields_panel.js')
    resolve(com.default)
})

// --------------field------------
Vue.component('com-sim-fields', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./fields_panels/sim_fields.js')
    resolve(com.com_sim_fields)
})
Vue.component('com-sim-fields-local', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./fields_panels/sim_fields_local.js')
    resolve(com.default)
})
Vue.component('com-suit-fields', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./fields_panels/suit_fields.js')
    resolve(com.suit_fields)
})
Vue.component('com-suit-fields-local', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./fields_panels/suit_fields_local.js')
    resolve(com.default)
})
// Vue.component('com-fields-table-block', async (resolve, reject)=> {
//     var com = await import(/* webpackChunkName: 'maybe_old' */'./fields_panels/fields_table_block.js')
//     resolve(com.default)
// })

Vue.component('com-layout-div', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./layout/layout_div.vue')
    resolve(com.default)
})

// --------------table_panels/ele_table  应该是某个时间心血来潮写的，现在全面使用com-d-table，这些全部淘汰
Vue.component('com-table-bus', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./table_panels/ele_table.js')
    resolve(com.ele_table)
})
Vue.component('com-table-bus-ops', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./table_panels/ele_table.js')
    resolve(com.ele_operations)
})
Vue.component('com-table-bus-filter', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./table_panels/ele_table.js')
    resolve(com.ele_filter)
})
Vue.component('com-table-bus-page', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'maybe_old' */'./table_panels/ele_table.js')
    resolve(com.ele_page)
})
