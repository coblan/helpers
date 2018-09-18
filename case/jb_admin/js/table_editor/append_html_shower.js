/*
以html形式显示  _html_field 的内容
* */
var append_html_shower = {
    props:['rowData','field','index'],
    template:`<span v-html="rowData['_html_'+field]"></span>`,

}

Vue.component('com-table-append-html-shower',append_html_shower)


