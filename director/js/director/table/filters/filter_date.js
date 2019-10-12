require('./styl/com_date.styl')
var com_date = {
    props: ['head', 'search_args'],
    template: `<div class="com-filter-date">
    <div v-if="head.label" v-text="head.label"></div>
    <com-field-date :head="head" :row="search_args"></com-field-date>
    </div>
    `,
}


Vue.component('com-filter-date',com_date)