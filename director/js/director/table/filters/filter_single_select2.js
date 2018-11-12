
var com_select = {
    props: ['head', 'search_args'],
    template: `<com-field-single-select2 :head="head" :row="search_args"></com-field-single-select2>
    `,
}


Vue.component('com-filter-single-select2',com_select)