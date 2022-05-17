// import pagination from "./table_group/pagination";
// import {ele_table} from "./table_group/table_grid";
// import {table_row} from "./table_group/table_rows";
// import {ele_operations} from "./table_group/operations";
// import {ele_filter} from "./table_group/filter";



Vue.component('com-table-pagination', async (resolve, reject)=> {

    var com = await import(/* webpackChunkName: 'table_group_import' */'./table_group_import.js')
    resolve(com.pagination)
})

Vue.component('com-table-grid', async (resolve, reject)=> {

    var com = await import(/* webpackChunkName: 'table_group_import' */'./table_group_import.js')

    resolve(com.ele_table)
})

Vue.component('com-table-rows', async (resolve, reject)=> {

    var com = await import(/* webpackChunkName: 'table_group_import' */'./table_group_import.js')

    resolve(com.table_row)
})

Vue.component('com-table-operations', async (resolve, reject)=> {

    var com = await import(/* webpackChunkName: 'table_group_import' */'./table_group_import.js')

    resolve(com.ele_operations)
})
Vue.component('com-table-filters', async (resolve, reject)=> {

    var com = await import(/* webpackChunkName: 'table_group_import' */'./table_group_import.js')

    resolve(com.ele_filter)
})
Vue.component('com-table-parents', async (resolve, reject)=> {

    var com = await import(/* webpackChunkName: 'table_group_import' */'./table_group_import.js')

    resolve(com.table_parents)
})
