import {com_fields_panel} from './fields_panel'

export default {
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

