<template>
    <div class="com-swiper-image" :style="mystyle" >
        <div class="mylabel" v-if="ctx.label" v-text="ctx.label"></div>
        <div class="for-click" @click="on_click" v-if="ctx.click_express"></div>
        <a class="for-click"  v-if="ctx.link_express" :href="get_link()"></a>
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
            },
            get_link(){
                return ex.eval(this.ctx.link_express,{vc:this})
            }
        },
        computed:{
            mystyle(){
                var dc = {
                    'background-image':'url('+this.ctx.image_url+')',
                }
//                if(this.ctx.click_express){
//                    dc['cursor'] = 'pointer'
//                }
                return dc
            }
        }
    }
</script>

<style scoped lang="scss">
    .com-swiper-image{
        position: relative;
    }
.for-click{
    /*background-color: red;*/
    display: inline-block;
    position: absolute;
    width: 60%;
    height: 60%;
    top:20%;
    left: 20%;
    cursor: pointer;
}
</style>
