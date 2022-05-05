import {suit_fields} from  './suit_fields'

export default {
    mixins:[suit_fields],
    methods:{
        submit:function(){
            if(this.isValid()){
                this.$emit('finish',this.row)
            }
        }
    }
}

// window.suit_fields_local=suit_fields_local

