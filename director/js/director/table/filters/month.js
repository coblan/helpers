
var com_month = {
    props: ['head', 'search_args'],
    template: `<com-field-month :head="head" :row="search_args"></com-field-month>
    `,
}


Vue.component('com-filter-month',com_month)