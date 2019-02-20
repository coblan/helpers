require('./scss/month.scss')

var com_month = {
    props: ['head', 'search_args'],
    template: `<div class="com-filter-month">
        <com-field-month :head="head" :row="search_args"></com-field-month>
        </div>
    `,
}


Vue.component('com-filter-month',com_month)