require('./scss/fields_panel.scss')

export var com_form_panel={
    props:['ctx'],
    data:function(){
        var self=this
        var option = {
            okBtn: self.ctx.okBtn || '确定',
            ops:self.ctx.ops,
        }
        if(this.ctx.option){
            ex.assign(option,this.ctx.option)
        }

        return {
            row:this.ctx.row || {},
            heads:this.ctx.heads,
            form: this.ctx.form || cfg.form || com_form,
            small:false,
            small_srn:ex.is_small_screen(),
            option:option

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
    template:`<div :class="['flex-v com-fields-panel',option.cssCls,{'small_srn':small_srn}]">
     <component class="msg-bottom" :is="form" :heads="heads" :row="row" :option="option" @finish="on_finish($event)"></component>
     </div>`,
}
window.com_form_panel = com_form_panel
Vue.component('com-form-panel',com_form_panel)