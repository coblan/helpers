<template>
    <div class="com-line-info">
        <div v-for="row in rows" v-text="row">

        </div>
    </div>
</template>

<script>
    export default {
        props:['ctx'],
        data(){
            return {
                rows: this.ctx.rows || []
            }
        },
        mounted(){
            if(this.ctx.mounted_express){
                ex.eval(this.ctx.mounted_express,{vc:this})
            }
        },
        methods:{
            appendRows(rows){
                this.rows = this.rows.concat(rows)
                Vue.nextTick(()=>{
                    this.$el.scrollTop = this.$el.scrollHeight;
                })

            }
        }
    }
</script>

<style scoped lang="scss">
    .com-line-info{
        height: 100%;
        overflow: auto;
        margin-left: 10px;
    }
</style>