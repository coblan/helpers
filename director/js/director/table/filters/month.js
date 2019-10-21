require('./scss/month.scss')

var com_month = {
    props: ['head', 'search_args'],
    template: `<div class="com-filter-month" >
        <span v-if="head.show_label"><span  v-text="head.label"></span>:</span>
        <com-field-month :head="head" :row="search_args"></com-field-month>
        </div>
    `,
    data(){
        if(! this.head.show_label){
            this.head.placeholder = this.head.placeholder || this.head.label
        }
        return {

        }
    }
}


Vue.component('com-filter-month',com_month)