<template>
    <van-field class="com-field-linetext"  v-model="inn_data" :required="head.required"
               :label="head.label"
               type="number"
               :placeholder="normed_placeholder"
               :name="head.name"
               autosize
               :error-message="head.error"
               :readonly="head.readonly"
               @blur="on_blur"
    >

    </van-field>
</template>
<script>
    export default {
        props:['head','row'],
        mounted:function(){
            if(!this.head.readonly){
                this.setup_validate_msg_router()
            }
        },
        data(){
            return {
                inn_data:this.row[this.head.name]
            }
        },
        watch:{
            row:{
                handler(nv){
                    this.inn_data = nv[this.head.name]
                },
                deep:true
            }
        },
        computed:{
//            out_data(){
//                debugger;
//                return this.row[this.head.name]
//            },
            normed_placeholder:function(){
                if(! this.head.readonly){
                    return this.head.placeholder || '请输入'+this.head.label
                }else{
                    return ''
                }
            }
        },
        methods:{
            setup_validate_msg_router(){
                if(!this.head.validate_showError){
                    Vue.set(this.head,'error','')
                    this.head.validate_showError="scope.head.error=scope.msg"
                }
                if(!this.head.validate_clearError){
                    this.head.validate_clearError="scope.head.error=''"
                }
            },
            on_blur(){
                if(this.inn_data || this.inn_data==0){
                    this.row[this.head.name] = parseFloat(this.inn_data)
                }else{
                    this.row[this.head.name] = ''
                }
            }
        }
    }
</script>
