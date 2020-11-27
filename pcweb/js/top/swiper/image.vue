<template>
    <div class="com-swiper-image" :style="mystyle" @click="on_click">
        <div class="mylabel" v-if="ctx.label" v-text="ctx.label"></div>
    </div>
</template>
<script>
    export default{
        props:['ctx'],
        mounted(){

        },
        methods:{
            on_click(){
                if(this.ctx.click_express){
                    ex.eval(this.ctx.click_express,{vc:this})
                }
            }
        },
        computed:{
            mystyle(){
                var dc = {
                    'background-image':'url('+this.ctx.image_url+')',
                }
                if(this.ctx.click_express){
                    dc['cursor'] = 'pointer'
                }
                return dc
            }
        }
    }
</script>
