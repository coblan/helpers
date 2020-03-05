<template>
    <div class="com-field-switch">
        <van-cell :title="head.label" >
            <van-switch v-model="checked"  active-color="#07c160" :disabled="head.readonly"/>
            <div class="field-error-msg" v-if="head.error" v-text="head.error" style="color: red"></div>
        </van-cell>
    </div>
</template>
<script>
    import {mix_validta_msg} from './mix_validate_msg'
    export default{
        props:['row','head'],
        data(){
            if(this.head.int_bool){
                if(this.row[this.head.name]==1){
                    var checked = true
                }else{
                    var checked = false
                }
            }else{
                var checked = this.row[this.head.name]
            }
            return {
                checked:checked
            }
        },
        mixins:[mix_validta_msg],
        watch:{
            checked(v){
                if(this.head.int_bool){
                    if(v){
                        this.row[this.head.name] =1
                    }else{
                        this.row[this.head.name] = 0
                    }
                }else{
                    this.row[this.head.name] = v
                }
            }
        }
    }
</script>