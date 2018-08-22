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
    mixins:[mix_fields_data,mix_nice_validator],
    template:` <div class="field-panel sim-fields" style="text-align:center;">
                <com-table-fields :heads="heads" :row="row">
                    <slot>
                    <tr>
                    <td colspan="2">
                        <div class="submit-block">
                            <button @click="submit" type="btn"
                                :class="['btn',btnCls]"><span v-text="okBtn"></span></button>
                        </div>
                     </td>
                    </tr>
                    </slot>
           </com-table-fields>
        </div>`,
    methods:{
        submit:function(){
            if(this.isValid()){
                this.$emit('submit')
            }
        }
    }
}

window.com_sim_fields = com_sim_fields

Vue.component('com-sim-fields',com_sim_fields)