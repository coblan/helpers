<template>
    <div class="com-field-el-select" :class="head.class">
        <el-select v-model="row[head.name]" filterable placeholder="请选择" size="small" :clearable="!head.required">
            <el-option
                    v-for="item in normed_options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
            </el-option>
        </el-select>
    </div>

</template>
<script>
    export default {
        props:['row','head'],
        data(){
            return {
                inn_value:this.row[this.head.name]
            }
        },
        mounted:function(){
            if(this.head.css){
                ex.append_css(this.head.css)
            }
        },

        computed:{
            value:function(){
                return this.row[this.head.name]
            },
            normed_options(){
                return this.head.options
            },
        },
        methods:{

        }

    }
</script>


