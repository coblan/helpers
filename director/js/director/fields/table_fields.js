require('./scss/table_fields.scss')

import {baseInput} from  '../inputs/basic'
var table_fields={
    props:['heads','row','inputWidth','labelWidth'],
    template:`<table class="table-fields">
        <tr v-for="(head,index) in heads" :class="{'last-input':index==heads.length-1}">
            <td class="field-label-td" :style="{width:labelWidth}" valign="top">
            <div class="field-label" style="position: relative">
                <span v-text="head.label"></span>
                <span class="req_star" v-if='head.required'>*</span>
            </div>

            </td>
            <td class="field-input-td"  :style="{width:inputWidth}">
            <div class="field-input">
                <component v-if="head.editor" :is="head.editor"
                     @field-event="$emit('field-event',$event)"
                     :head="head" :row="row"></component>
                <span v-else v-text="row[head.name]"></span>
                <span class="help-text clickable">
                    <i style="color: #3780af;position: relative;top:10px;"  v-if="head.help_text" @click="show_msg(head.help_text,$event)" class="fa fa-question-circle" ></i>
                </span>
            </div>

            </td>
        </tr>
        <slot></slot>
    </table>`,
    methods:{
        show_msg:function(msg,event){
            layer.tips(msg, event.target);
        }
    },
    components:baseInput,
}



Vue.component('com-table-fields',table_fields)