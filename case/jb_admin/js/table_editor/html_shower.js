
var bool_shower = {
    props:['rowData','field','index'],
    template:`<span v-html="rowData[field]"></span>`,

}

Vue.component('com-table-html-shower',bool_shower)


