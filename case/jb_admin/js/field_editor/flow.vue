<template>
    <div class="com-field-flow">
        <div class="mermaid" v-text="graph"></div>

        <span style="color: #8c8c8c;font-size: 90%">当前可选项:</span>
        <el-select v-if="next_options.length>0" v-model="row[head.name]" placeholder="请选择" size="small" :clearable="!head.required" :id="'id_'+head.name" :name="head.name">
            <el-option
                    v-for="item in next_options"
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
                graph:'' ,//'graph LR;A --> B[审核中];B --> C[审核完毕];',
                rendered:false,
                next_options:[]
            }
        },
        computed:{
            value(){
                return this.row[this.head.name]
            },
//            myoptions(){
//                var value = this.value
//                if(value == undefined ){
//                    return []
//                }
//                var next_list = this.head.chain[value].next
//                next_list.push(value)
//                var next_options = ex.filter(this.head.options,(item)=>{
//                            return ex.isin(item.value,next_list)
//                        })
//                return next_options
//            }
        },
        watch:{
            value(nv){
                var value = this.row[this.head.name]
               if(value== undefined || this.rendered){
                   return
               }
                this.init_option()

                var graph_logic = this.head.chain[value].last
                this.graph = 'graph TD;'
                var crt_label = ex.findone(this.head.options,{value:value}).label
                var label_list =[]
                ex.each(graph_logic,item=>{
                    var label = ex.findone(this.head.options,{value:item}).label
                    label_list.push(label)
            })
                label_list.push(crt_label)

                for(var i=0;i<label_list.length;i++){
                    if(i+1 < label_list.length){
                        this.graph += label_list[i]+'-->'+label_list[i+1]+';'
                    }else {
                        this.graph += label_list[i]
                    }
                }

                ex.load_js('https://cdn.jsdelivr.net/npm/mermaid@8.5.2/dist/mermaid.min.js').then(()=>{
//                mermaid.initialize({startOnLoad:false});
                    setTimeout(()=>{
                    mermaid.init(undefined,$(this.$el).find('.mermaid') )
                    this.rendered = true
                },200)
            })
            }
        },
        methods:{
            init_option(){
                var value = this.value
                var next_list = this.head.chain[value].next
                next_list.push(value)
                var next_options = ex.filter(this.head.options,(item)=>{
                            return ex.isin(item.value,next_list)
                        })
                this.next_options = next_options
            }
        }
    }
</script>
<style scoped lang="scss">

</style>