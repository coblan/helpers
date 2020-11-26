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
    import field_number from './field_number.vue'
    export default {
        props:['head','row'],
        mixins:[field_number],
        methods:{
            on_blur(){
                if(this.inn_data || this.inn_data==0){
                    this.row[this.head.name] = parseInt(this.inn_data)
                }else{
                    this.row[this.head.name] = ''
                }
            }
        }
    }
</script>