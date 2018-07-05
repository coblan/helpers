require('./scss/table_fields.scss')

import {baseInput} from  '../inputs/basic'
var table_fields={
    props:['heads','row','inputWidth','labelWidth'],
    template:`<table class="table-fields">
        <tr v-for="head in heads">
            <td class="field-label" :style="{width:labelWidth}" valign="top">
            <div style="position: relative">
                <span v-text="head.label"></span>
                <span class="req_star" style="position: absolute;right: -0.5em;top:0" v-if='head.required'>*</span>
            </div>

            </td>
            <td  :style="{width:inputWidth}">
            <div class="field-input">
                <component v-if="head.editor" :is="head.editor" :head="head" :row="row"></component>
                <span v-else v-text="row[head.name]"></span>
            </div>



            </td>
        </tr>
        <slot></slot>
    </table>`,
    components:baseInput,
}
Vue.component('com-table-fields',table_fields)