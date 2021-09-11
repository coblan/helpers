<template>
    <div class="com-field-bool">

        <el-switch
                v-model="row[head.name]"
                active-color="#13ce66"
                inactive-color="#999"
                :name="head.name"
                :disabled="head.readonly"
        >
        </el-switch>

    </div>
</template>
<script>
    export default {
        props:['row','head'],
        mounted(){
            if(this.head.css){
                ex.append_css(this.head.css)
            }
        },
        computed:{
            my_label:function(){
                if(this.head.check_label){
                    return this.head.check_label
                }else{
                    return this.head.label
                }
            }
        }
    }
</script>

