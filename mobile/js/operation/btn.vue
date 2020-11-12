<template>
    <van-button class="com-btn" :class="ctx.class" :type="ctx.type || 'primary'" @click="on_click()" size="large">
        <span v-text="ctx.label || '确定'"></span>
    </van-button>
</template>
<script>
export default {
    props:['ctx'],
    data(){
        let parStore = ex.vueParStore(this)
        return {
            parStore:parStore
        }
    },
    mounted(){
        if(this.ctx.css){
            ex.append_css(this.ctx.css)
        }
    },
    methods:{
        on_click:function(){
            var click_express = this.ctx.click_express || this.ctx.action
            if( click_express ){
                ex.eval( click_express ,{ps:this.parStore,head:this.ctx,vc:this})
            }else{
                this.$emit('action')
            }

        }
    }

}
</script>
