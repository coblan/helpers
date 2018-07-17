
Vue.component('com-sim-fields',{
    props:{
        heads:'',
        row:'',
        okBtn:{
            default:function(){
                return '确定'
            }
            },
        exClass:''
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
    template:` <div class="field-panel" style="text-align:center;">
                <com-table-fields :heads="heads" :row="row"
                    input-width="23em" label-width="8em"
                    style="width: 30em;text-align: left;display: inline-block;">
                    <slot>
                    <tr>
                    <td></td>
                    <td>
                    <button @click="submit"
                        style="width: 100%;position: relative;" type="btn"
                            class="btn btn-primary btn-sm"><span v-text="okBtn"></span></button></td>
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
})