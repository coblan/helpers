require('./scss/sim_fields.scss')

export var com_sim_fields = {
    props:{
        heads:'',
        row:'',
        okBtn:{
            default:function(){
                return '确定'
            }
            },
        crossBtn:'',
        autoWidth:{
            default:function(){
                return true
            }
        },
        btnCls:{
            default:function(){
                return 'btn-primary btn-sm'
            }
        }
        },
    data:function (){
        return {
            small_srn:ex.is_small_screen(),
            small:false
        }
    },
    mounted:function(){
        // 由于与nicevalidator 有冲突，所以等渲染完成，再检测
        setTimeout(function(){
            if($(this.$el).width() <600 ){
                this.small=true
            }else{
                this.small=false
            }
        },10)

    },
    computed:{
        normed_heads:function(){
            return this.heads
        },
        label_width:function (){
            if(!this.autoWith){

            }
            var max=4
            ex.each(this.heads,function(head){
                if(max < head.label.length){
                    max=head.label.length
                }
            })
            max+=1
            return {width:max+'em'}
        }
    },
    //created:function(){
    //    if(!this.okBtn){
    //        this.okBtn='确定'
    //    }
    //},
    components:window._baseInput,
    mixins:[mix_fields_data,mix_nice_validator],
    template:` <div :class="['field-panel sim-fields',{'small':small,'msg-bottom':small}]"
    style="text-align:center;">
           <table class="table-fields">
        <tr v-for="head in heads">
            <td class="field-label-td"  valign="top" >
            <div class="field-label" :style="label_width">
                <span class="label-content">
                     <span v-text="head.label"></span>
                     <span class="req_star" v-if='head.required'>*</span>
                </span>


            </div>

            </td>
            <td class="field-input-td" >
                <div class="field-input">
                    <component v-if="head.editor" :is="head.editor"
                         @field-event="$emit('field-event',$event)"
                         :head="head" :row="row"></component>

                </div>
            </td>
            <td>
                <span v-if="head.help_text" class="help-text clickable">
                            <i style="color: #3780af;position: relative;top:10px;"   @click="show_msg(head.help_text,$event)" class="fa fa-question-circle" ></i>
                </span>
            </td>
        </tr>
        <slot :row="row">
            <!--按钮横跨两列 ！小尺寸时 强制 -->
             <tr v-if="crossBtn || small" class="btn-row">
                <td class="field-input-td" colspan="3">
                    <div class="submit-block">
                        <button @click="submit" type="btn"
                            :class="['form-control btn',btnCls]"><span v-text="okBtn"></span></button>
                    </div>
                </td>
            </tr>
            <!--按钮在第二列-->
               <tr v-else class="btn-row">
                   <td class="field-label-td"></td>
                    <td class="field-input-td" colspan="1">
                        <div class="submit-block">
                            <button @click="panel_submit" type="btn"
                                :class="['btn',btnCls]"><span v-text="okBtn"></span></button>
                        </div>
                     </td>
                     <td></td>
               </tr>
        </slot>

    </table>


        </div>`,
    methods:{

        panel_submit:function(){
            if(this.$listeners && this.$listeners.submit){
                if(this.isValid()){
                    this.$emit('submit',this.row)
                }
            }else{
                this.submit()
            }

        },
        show_msg:function(msg,event){
            layer.tips(msg, event.target);
        },
        after_save:function(row){
            this.$emit('after-save',row)
        }

    }
}

window.com_sim_fields = com_sim_fields

Vue.component('com-sim-fields',com_sim_fields)