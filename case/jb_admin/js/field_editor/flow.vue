<template>
    <div class="com-field-flow">
        <div class="mermaid" v-text="graph"></div>
    </div>
</template>
<script>
    export default {
        props:['row','head'],
        data(){
            return {
                graph:'' //'graph LR;A --> B[审核中];B --> C[审核完毕];',
            }
        },
        computed:{
            value(){
                return this.row[this.head.name]
            }
        },
        watch:{
            value(nv){
                var value = this.row[this.head.name]
               if(value== undefined){
                   return
               }
                var graph_logic = this.head.chain[value].last
                this.graph = 'graph LR;'
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
                },200)
            })
            }
        },
        mounted(){

        }
    }
</script>
<style lang="scss">
.cssClass{
    color: red;
}
</style>