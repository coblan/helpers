Vue.component('com-uis-nav-bar',{
    props:{
        title:'',
        back:'',
        ops:{default:()=>{return []}}},
    template:`<div class="com-uis-nav-bar"><van-nav-bar
            :title="title"
            :left-arrow="back"
            @click-right="onClickRight"
            @click-left="onClickLeft">
        <van-icon v-if="ops.length>0" name="bars" slot="right" />
    </van-nav-bar>
        <van-actionsheet
            v-model="actionVisible"
            :actions="ops"
            cancel-text="取消"
            @select="onSelectAction"
    ></van-actionsheet>
    </div>`,
    data(){
        this.ops = this.ops || []
        return {
            parStore:ex.vueParStore(this),
            actionVisible:false,
        }
    },
    computed:{
        //normed_ops(){
        //    var myops=[]
        //    this.ops.forEach(item=>{
        //        myops.push({name:item.label,action:item.action})
        //    })
        //    return myops
        //}
    },
    methods:{
        onClickLeft(){
            history.back()
        },
        onClickRight(){
            this.actionVisible = true
        },
        onSelectAction(action){
            ex.eval(action.action,{ps:this.parStore,head:action})
            this.actionVisible =false
        }
    }
})