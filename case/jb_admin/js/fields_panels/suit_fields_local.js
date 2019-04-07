import {suit_fields} from  './suit_fields'

var suit_fields_local={
    mixins:[suit_fields],
    methods:{
        submit:function(){
            if(this.isValid()){
                this.$emit('finish',this.row)
            }
        }
    }
}

window.suit_fields_local=suit_fields_local

Vue.component('com-suit-fields-local',suit_fields_local)