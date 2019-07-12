/*
用在fields表单里面的mixins

增加nicevalidator功能
* */

var nice_validator={
    mounted:function(){
            this.update_nice()
    },
    computed:{
        head_fv_rules(){
            var ls=[]
            ex.each(this.heads,head=>{
                var tmp=''
                if(head.required){
                    tmp+='required'
                }
                if(head.fv_rule){
                    tmp += head.fv_rule
                }
                ls.push(head.name+ tmp)
            })
            return ls.join(';')
        }
    },
    watch:{
        head_fv_rules(){
            this.update_nice()
        }
    },
    //watch:{
    //    heads:function(new_heads,old_heads){
    //        for(let i=0;i<new_heads.length;i++){
    //            let new_head = new_heads[i]
    //            let old_head = old_heads[i]
    //            if(new_head!=old_head){
    //                let new_rule = this.get_head_fv_rule(new_head)
    //                let old_rule = this.get_head_fv_rule(old_head)
    //                if(new_rule != old_rule){
    //                    this.nice_validator.setField(new_head.name,new_rule)
    //                }
    //            }
    //        }
    //    }
    //},
    methods:{
        get_head_fv_rule:function(head){
            // todo  判断 该函数应该是没有用了，注意删除
            var ls =[]
            if(head.fv_rule){
                ls.push(head.fv_rule)
            }
            if( head.required){
                if(!head.fv_rule || head.fv_rule.search('required')==-1){// 规则不包含 required的时候，再添加上去
                    ls.push('required')
                }
            }
            if(head.validate_showError){
                return {
                    rule:ls.join(';'),
                    msg:head.fv_msg,
                    msgClass:'hide',
                    invalid:function(e,b){
                        var label =head.label
                        ex.eval(head.validate_showError,{msg:label+' : '+b.msg})
                    },
                }
            }else{
                return {
                    rule:ls.join(';'),
                    msg:head.fv_msg
                }
            }

        },
        update_nice:function(){
            var self=this
            var validate_fields={}
            ex.each(this.heads,function(head){
                var ls=[]
                if(head.readonly){
                    return
                }
                if(head.fv_rule){
                    ls.push(head.fv_rule)
                }
                if( head.required){
                    if(!head.fv_rule || head.fv_rule.search('required')==-1){// 规则不包含 required的时候，再添加上去
                        ls.push('required')
                    }
                }

                if(head.validate_showError){
                    validate_fields[head.name]={
                        rule:ls.join(';'),
                        msg:head.fv_msg,
                        msgClass:'hide',
                        invalid:function(e,b){
                            var label =head.label
                            ex.eval(head.validate_showError,{msg:b.msg,head:head})
                        },
                        valid : function(element, result){
                             ex.eval(head.validate_clearError,{head:head})
                         }
                    }
                }else{
                        validate_fields[head.name]={
                            rule:ls.join(';'),
                            msg:head.fv_msg,

                        }
                }

            })
            this.nice_validator =$(this.$el).validator({
                fields: validate_fields,
                //msgShow:function($msgbox, type){
                //    alert('aajjyy')
                //},validation: function(element, result){
                //   alert('aaabbbb')
                //}
            });

        },
        isValid:function(){
            var nice_rt = this.nice_validator.isValid()
            return nice_rt
            //var totalValid=[nice_rt]
            //var totalValid=ex.vueBroadCall(this,'isValid')
            //totalValid.push(nice_rt)
            //
            ////ex.each(this.$children,function(child){
            ////    if(child.isValid){
            ////        totalValid.push(child.isValid())
            ////    }
            ////})
            //
            //var valid =true
            //ex.each(totalValid,function(item){
            //    valid = valid && item
            //})
            //return valid
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
            var real_input = $(this.$el).find('.real-input')
            if(real_input.length !=0){
                real_input.trigger("showmsg", ["error", errors[k].join(';')]);
            }

            for(var k in errors){
                var head = ex.findone(this.heads,{name:k})
                if(head && head.validate_showError){
                    ex.eval(head.validate_showError,{head:this.head,msg:errors[k].join(';')})
                }else{
                    $(this.$el).find('[name='+k+']').trigger("showmsg", ["error", errors[k].join(';')]);
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