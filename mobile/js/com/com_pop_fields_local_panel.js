import {com_pop_fields_panel} from './com_pop_fields_panel'
var com_pop_fields_local_panel={
    mixins:[com_pop_fields_panel],
    methods:{
        submit:function(){
            if(this.isValid()){
                this.$emit('finish',this.row)
            }
        }
    }

}
window.com_pop_fields_local_panel = com_pop_fields_local_panel
Vue.component('com-pop-fields-local-panel',com_pop_fields_local_panel)