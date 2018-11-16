require('./scss/fields_local_panel.scss')

var fields_local_panel={
    props:['ctx'],
    data:function(){
        return {
            row:this.ctx.row,
            heads:this.ctx.heads,
            ops:this.ctx.ops,
            fields_editor: this.ctx.fields_editor || com_sim_fields
        }
    },
    methods:{
        submit:function(e){
            var row = e
            if(this.$refs.fields.isValid()){
                this.$emit('finish',row)
            }
        }
    },
    template:`<div class="flex-v com-fields-local-panel">
     <component ref="fields" class="msg-bottom" :is="fields_editor" :heads="heads" :row="row" @submit="submit($event)"></component>
     <!--<div style="text-align: right;padding: 8px 3em;">-->
        <!--<component v-for="op in ops" :is="op.editor" @operation="on_operation(op)" :head="op"></component>-->
    <!--</div>-->
     </div>`,
}

window.fields_local_panel=fields_local_panel
Vue.component('com-fields-local-panel',fields_local_panel)