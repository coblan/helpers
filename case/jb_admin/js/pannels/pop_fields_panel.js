import {com_fields_panel} from './fields_panel'

var com_pop_fields_panel = {
    props:['ctx'],
    data:function(){
        return {
            fields_editor: this.ctx.fields_editor || com_pop_field,
        }
    },
    mixins:[com_fields_panel],
    template:`<div :class="['flex-v com-fields-panel',cssCls,{'small_srn':small_srn}]" style="height: 100%">
     <component class="msg-bottom"  :is="fields_editor" :heads="heads" :row="row" :ops="ops"
       :cross-btn="crossBtn" @finish="on_finish($event)"></component>
     </div>`,
}

Vue.component('com-panel-pop-fields',com_pop_fields_panel)