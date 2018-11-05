require('./scss/com_pop_fields_panel.scss')

export var com_pop_fields_panel={
    props:['ctx'],
    data:function(){
        return {
            row:this.ctx.row,
            heads:this.ctx.heads,
            ops:this.ctx.ops,
            fields_editor: this.ctx.fields_editor || com_sim_fields
        }
    },
    mixins:[],
    methods:{
    },
    template:`<div class="flex-v com-pop-fields-panel">
     <component class="msg-bottom" :is="fields_editor" :heads="heads" :row="row" @after-save="$emit('finish',$event)"></component>
     <div style="text-align: right;padding: 8px 3em;">
        <component v-for="op in ops" :is="op.editor" @operation="on_operation(op)" :head="op"></component>
    </div>
     </div>`,
}
window.com_pop_fields_panel = com_pop_fields_panel
Vue.component('com-pop-fields-panel',com_pop_fields_panel)