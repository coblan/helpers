
Vue.component('com-filter-search-select', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'table_filter' */'./filter_editor/search_select.vue')
    resolve(com.default)
})
Vue.component('com-filter-check', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'table_filter' */'./filter_editor/check.vue')
    resolve(com.default)
})
Vue.component('com-filter-compare', async (resolve, reject)=> {
    var com = await import(/* webpackChunkName: 'table_filter' */'./filter_editor/compare.js')
    resolve(com.default)
})