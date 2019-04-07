
var com_select = {
    props: ['head', 'search_args'],
    template: `<com-field-single-chosen :head="head" :row="search_args"></com-field-single-chosen>
    `,
}


Vue.component('com-filter-search-select',com_select)