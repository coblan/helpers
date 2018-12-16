require('./scss/fields_panel.scss')

export var com_fields_panel={
    props:['ctx'],
    data:function(){
        return {
            row:this.ctx.row || {},
            heads:this.ctx.heads,
            ops:this.ctx.ops,
            fields_editor: this.ctx.fields_editor || cfg.fields_editor || com_sim_fields,
            small:false,
            small_srn:ex.is_small_screen(),
            cssCls:'',
            crossBtn:this.ctx.crossBtn || '',
            okBtn: this.ctx.okBtn || '确定',
        }
    },
    mounted:function(){
        if($(this.$el).width() <600 ){
            this.small=true
        }else{
            this.small=false
        }
    },
    methods:{
        on_finish:function(e){
            this.$emit('finish',e)
        }
    },
    template:`<div :class="['flex-v com-fields-panel',cssCls,{'small_srn':small_srn}]">
     <component class="msg-bottom" :is="fields_editor" :heads="heads" :row="row" :ok-btn="okBtn"
       :cross-btn="crossBtn" @finish="on_finish($event)"></component>
     </div>`,
}
window.com_fields_panel = com_fields_panel
Vue.component('com-fields-panel',com_fields_panel)
Vue.component('com-panel-fields',com_fields_panel)