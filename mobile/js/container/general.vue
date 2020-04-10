<template>
    <div class="com-list-general list-content">
        <div v-for="row in rows">
            <component :is="parStore.vc.ctx.row_editor" :ctx="row"></component>
        </div>
    </div>
</template>
<script>
export default   {
    props:['heads','rows'],
    data(){
        var parStore = ex.vueParStore(this)
        return {
            parStore:parStore
        }
    },
    mounted(){
        if(this.option && this.option.css){
            ex.append_css(this.option.css)
        }
    },
    computed:{

    },
    methods:{
        on_click(row){
            if(this.parStore.vc.ctx.action){
                ex.eval(this.parStore.vc.ctx.action,{row:row,ps:this.parStore})
            }
        }
    }

}


</script>
