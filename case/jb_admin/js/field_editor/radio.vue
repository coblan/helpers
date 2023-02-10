<template>
    <div class="com-field-radio">
        <input type="text" v-model='row[head.name]' style="display: none" :name="head.name">
        <span v-if="head.readonly" v-text="mylabel"></span>

            <el-radio-group  v-else v-model="row[head.name]">
                <el-radio v-for="opt in head.options" :label="opt.value" >
                    <span v-text="opt.label"></span>
                </el-radio>
            </el-radio-group>
        <!--<template v-else>-->
            <!--<div v-for="op in head.options" style="display: inline-block;margin: 0 3px">-->
                <!--<input type="radio" :id="'_radio'+head.name+op.value"-->
                       <!--:value="op.value" v-model='row[head.name]'>-->
                <!--<label :for="'_radio'+head.name+op.value" v-text="op.label" style="font-weight: 400;"></label>-->
            <!--</div>-->
        <!--</template>-->
    </div>
</template>
<script>
    export default {
        props:['row','head'],
        computed:{
            mylabel:function(){
                var one = ex.findone(this.head.options,{value:this.row[this.head.name]})
                if(one){
                    return one.label
                }else{
                    return ''
                }
            }
        }
    }
</script>
<style scoped lang="scss">
.com-field-radio{
  position: relative;
  top: 2px;
}
</style>
