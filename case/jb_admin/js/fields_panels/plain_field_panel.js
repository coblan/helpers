/*
* 可能无用了。
* */

require('./scss/plain_field_panel.scss')

var com_plain_fields = {
    props:{
        heads:'',
        row:'',
        okBtn:{
            default:function(){
                return '确定'
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
        }
    },
    created:function(){
        if(!this.okBtn){
            this.okBtn='确定'
        }
    },
    components:window._baseInput,
    mixins:[mix_fields_data,mix_nice_validator],
    template:` <div class="field-panel plain-field-panel">
        <div class="field" v-for="head in heads">
            <label for="" v-text="head.label"></label>
            <span class="req_star" v-if='head.required'>*</span>
             <span v-if="head.help_text" class="help-text clickable">
                    <i style="color: #3780af;position: relative;top:10px;" @click="show_msg(head.help_text,$event)" class="fa fa-question-circle" ></i>
              </span>
              <div class="field-input">
                <component v-if="head.editor" :is="head.editor"
                     @field-event="$emit('field-event',$event)"
                     :head="head" :row="row"></component>
            </div>

        </div>

        <div class="submit-block">
            <button @click="panel_submit" type="btn"
                :class="['btn',btnCls]"><span v-text="okBtn"></span></button>
        </div>
        </div>`,
    methods:{
        panel_submit:function(){
            if(this.isValid()){
                this.$emit('submit')
            }
        },
        show_msg:function(msg,event){
            layer.tips(msg, event.target);
        }
    }
}

window.com_plain_fields = com_plain_fields

Vue.component('com-plain-field-panel',com_plain_fields)