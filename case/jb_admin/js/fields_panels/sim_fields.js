require('./scss/sim_fields.scss')

var com_sim_fields = {
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
    template:` <div class="field-panel sim-fields" style="text-align:center;">
                <!--<com-table-fields :heads="heads" :row="row">-->
                    <!--<slot>-->
                    <!--<tr>-->
                        <!--<td colspan="2">-->
                            <!--<div class="submit-block">-->
                                <!--<button @click="panel_submit" type="btn"-->
                                    <!--:class="['btn',btnCls]"><span v-text="okBtn"></span></button>-->
                            <!--</div>-->
                         <!--</td>-->
                    <!--</tr>-->
                    <!--</slot>-->
           <!--</com-table-fields>-->

           <table class="table-fields">
        <tr v-for="head in heads">
            <td class="field-label-td"  valign="top">
            <div class="field-label" style="position: relative">
                <span v-text="head.label"></span>
                <span class="req_star" v-if='head.required'>*</span>
            </div>

            </td>
            <td class="field-input-td" >
            <div class="field-input">
                <component v-if="head.editor" :is="head.editor"
                     @field-event="$emit('field-event',$event)"
                     :head="head" :row="row"></component>
                <span v-if="head.help_text" class="help-text clickable">
                    <i style="color: #3780af;position: relative;top:10px;"   @click="show_msg(head.help_text,$event)" class="fa fa-question-circle" ></i>
                </span>
            </div>

            </td>
        </tr>

           <tr>
           <td class="field-label-td"></td>
                <td colspan="1">
                    <div class="submit-block">
                        <button @click="submit" type="btn"
                            :class="['btn',btnCls]"><span v-text="okBtn"></span></button>
                    </div>
                 </td>
           </tr>
    </table>


        </div>`,
    methods:{
        //panel_submit:function(){
        //    if(this.isValid()){
        //        this.$emit('submit')
        //    }
        //},
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