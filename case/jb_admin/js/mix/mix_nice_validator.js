/*
用在fields表单里面的mixins

增加nicevalidator功能
* */

var nice_validator={
    mounted:function(){
        this.update_nice()

    },
    methods:{
        update_nice:function(){
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
            if($(this.$el).hasClass('field-panel')){
                this.nice_validator =$(this.$el).validator({
                    fields: validator,
                });
            }else{
                this.nice_validator =$(this.$el).find('.field-panel').validator({
                    fields: validator,
                });
            }
        },
        isValid:function(){
            var nice_rt = this.nice_validator.isValid()
            //var totalValid=[nice_rt]
            var totalValid=ex.vueBroadCall(this,'isValid')
            totalValid.push(nice_rt)

            //ex.each(this.$children,function(child){
            //    if(child.isValid){
            //        totalValid.push(child.isValid())
            //    }
            //})

            var valid =true
            ex.each(totalValid,function(item){
                valid = valid && item
            })
            return valid
        },
        //before_save:function(){
        //    ex.vueSuper(this,{mixin:nice_validator,fun:'before_save'})
        //    if(this.isValid()){
        //        return 'continue'
        //    }else{
        //        return 'break'
        //    }
        //},
        showErrors:function(errors){
            for(var k in errors){
                //var head = ex.findone(this.heads,{name:k})
                var real_input = $(this.$el).find('.real-input')
                if(real_input.length !=0){
                    real_input.trigger("showmsg", ["error", errors[k].join(';')]);
                }else{
                    $(this.$el).find('#id_'+k).trigger("showmsg", ["error", errors[k].join(';')]);
                }
            }
        }
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