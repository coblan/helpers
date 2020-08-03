<template>
    <div class="com-field-el-select" :class="head.class">
        <span v-if='head.readonly' v-text='get_label(head.options,row[head.name])'></span>
        <div>
            <input type="text" style="display: none" :id="'id_'+head.name" :name="head.name" v-model="row[head.name]">
            <el-select v-model="row[head.name]" filterable placeholder="请选择" size="small" :clearable="!head.required"
                       :id="'id_'+head.name" :name="head.name">
                <el-option
                        v-for="item in normed_options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                </el-option>
            </el-select>
        </div>

    </div>

</template>
<script>
    export default {
        props:['row','head'],
        data(){
            return {
                inn_value:this.row[this.head.name],
                options:this.head.options || [],
                parStore:ex.vueParStore(this)
            }
        },
        mounted:function(){
            if(this.head.css){
                ex.append_css(this.head.css)
            }
            if(this.head.mounted_express){
                ex.eval(this.head.mounted_express,{vc:this,row:this.row,head:this.head})
            }
        },

        computed:{
            value:function(){
                return this.row[this.head.name]
            },
            normed_options(){
                return this.options
            },
        },
        methods:{

        }

    }
</script>


