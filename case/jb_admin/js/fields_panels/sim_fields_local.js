import {com_sim_fields} from  './sim_fields'

export  default  {
    mixins:[com_sim_fields],
    methods:{
        submit:function(){
            if(this.isValid()){
                this.$emit('finish',this.row)
            }
        }
    }
}

// window.com_sim_fields_local=com_sim_fields_local
//
// Vue.component('com-sim-fields-local',com_sim_fields_local)