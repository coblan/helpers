require('./styl/datetime.styl')
var com_date = {
    props: ['head', 'search_args'],
    template: `<div class="com-filter-datetime">
    <div v-if="head.label" v-text="head.label"></div>
    <com-field-datetime :head="head" :row="search_args"></com-field-datetime>
    </div>
    `,
}


Vue.component('com-filter-datetime',com_date)