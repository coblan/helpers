require('./scss/fields_panel.scss')

export var com_fields_panel={
    props:['ctx'],
    data:function(){
        return {
            row:this.ctx.row || {},
            heads:this.ctx.heads,
            ops:this.ctx.ops,
            fields_editor: this.ctx.fields_editor || cfg.fields_editor || com_sim_fields,
            is_mobile: !ex.device.pc,
            cssCls:'',
            okBtn: this.ctx.okBtn || '确定',
        }
    },
    methods:{
        on_finish:function(e){
            this.$emit('finish',e)
        }
    },
    template:`<div :class="['flex-v com-fields-panel',cssCls,{'mobile':is_mobile}]">
     <component class="msg-bottom" :is="fields_editor" :heads="heads" :row="row" :ok-btn="okBtn" @finish="on_finish($event)"></component>
     <!--<div style="text-align: right;padding: 8px 3em;">-->
        <!--<component v-for="op in ops" :is="op.editor" @operation="on_operation(op)" :head="op"></component>-->
    <!--</div>-->
     </div>`,
}
window.com_fields_panel = com_fields_panel
Vue.component('com-fields-panel',com_fields_panel)