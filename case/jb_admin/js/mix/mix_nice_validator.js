/*
用在fields表单里面的mixins

增加nicevalidator功能
* */

var nice_validator={
    mounted:function(){
        var self=this
        var validator={}
        ex.each(this.heads,function(head){
            var ls=[]

            if(head.fv_rule){
                ls.push(head.fv_rule)
            }
            if( head.required){
                if(!head.fv_rule || head.fv_rule.search('required')==-1){// 规则不包含 required的时候，再添加上去
                    ls.push('required')
                }
            }
            validator[head.name]=ls.join(';')
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