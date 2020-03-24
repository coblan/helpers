<template>
    <div class="com-uis-many-ops">
        <!--@click-right="onClickRight"-->
        <van-nav-bar
                :title="ctx.title"
                :left-arrow="can_back"
                @click-left="onClickLeft">
            <div slot="right">
                <component v-for="op in right_top"  :is="op.icon_editor" :ctx="op.icon_ctx"
                           @click.native="on_click(op)"></component>
                <van-icon @click.native="actionVisible=true" v-if="rigth_down.length > 0"  name="bars" slot="right" />
            </div>

        </van-nav-bar>
        <van-action-sheet
                v-model="actionVisible"
                :actions="rigth_down"
                cancel-text="取消"
                @select="onSelectAction"
        ></van-action-sheet>
    </div>
</template>
<script>
export default {
    props:['ctx'],
    data(){
        this.ops = this.ctx.ops || []
        return {
            parStore:ex.vueParStore(this),
            actionVisible:false,
        }
    },
    computed:{
        can_back(){
            if(this.ctx.back_action){
                return true
            }else{
                return  this.$root.stack.length >1
            }
        },
        right_top(){
            var myops = ex.filter(this.ops,(item)=>{
                        return item.level=='rigth-top'
                    })
            return myops
        },
        rigth_down(){
            var myops=[]
            let left_ops = ex.filter(this.ops,(item)=>{
                        return !item.level
                    })
            ex.each(left_ops,(item)=>{
                myops.push({name:item.label,action:item.action})
        })
            return myops
        }
    },
    methods:{
        onClickLeft(){
            if(this.ctx.back_action){
                ex.eval(this.ctx.back_action)
            }else{
                history.back()
            }
        },
        on_click(op){
            ex.eval(op.action,{ps:this.parStore,head:op})
        },
        onSelectAction(action){
            ex.eval(action.action,{ps:this.parStore,head:action})
            this.actionVisible =false
        }
    }
}
</script>
