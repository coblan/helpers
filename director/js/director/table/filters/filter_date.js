
var com_date = {
    props: ['head', 'search_args'],
    template: `<com-field-date :head="head" :row="search_args"></com-field-date>
    `,
}


Vue.component('com-filter-date',com_date)