
var bool_shower = {
    props:['rowData','field','index'],
    template:`<span>
    <i v-if="rowData[field]" style="color: green" class="fa fa-check-circle"></i>
    <i v-else style="color: red" class="fa fa-times-circle"></i>
    </span>`,

}

Vue.component('com-table-bool-shower',bool_shower)
