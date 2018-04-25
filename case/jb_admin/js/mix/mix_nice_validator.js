var nice_validator={
    mounted:function(){
        var self=this
        var validator={}
        ex.each(this.heads,function(head){
            if(head.required){
                validator[head.name]='required'
            }
        })
        this.nice_validator =$(this.$el).find('.field-panel').validator({
            fields: validator,
        });
    },
    methods:{
        before_save:function(){
            ex.vueSuper(this,{mixin:nice_validator,fun:'before_save'})
            //this.setErrors({})
            //eventBus.$emit('sync_data')
            if(this.nice_validator.isValid()){
                return 'continue'
            }else{
                return 'break'
            }
        },
    }
}

//$.validator.config({
//    rules: {
//        error_msg: function(ele,param){
//
//        }
//    }
//}
//
//);

window.mix_nice_validator=nice_validator