
var com_select = {
    props: ['head', 'search_args'],
    template: `<div class="form-control input-sm" >
            <com-field-search-select :head="head" :row="search_args"></com-field-search-select>
    </div>`,
}


Vue.component('com-filter-search-select',com_select)