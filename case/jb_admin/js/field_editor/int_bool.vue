<template>
    <div class="com-field-bool">
        <el-switch
                v-model="my_value"
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
            if(this.row[this.head.name] ==undefined){
                this.row[this.head.name] = 0
            }
        },
        computed:{
            my_value:{
                set:function(v){
                    if(v){
                        this.row[this.head.name] = 1
                    }else{
                        this.row[this.head.name] = 0
                    }
                },
                get:function(){
                    return Boolean(parseInt( this.row[this.head.name]) )
                }
            }
        }
    }
</script>
