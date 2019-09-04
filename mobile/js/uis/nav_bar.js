
Vue.component('com-uis-nav-bar',{
    props:{
        title:'',
        back:'',
        ops:{default:()=>{return []}}},
    template:`<div class="com-uis-many-ops">
 <!--@click-right="onClickRight"-->
    <van-nav-bar
            :title="title"
            :left-arrow="back"
            @click-left="onClickLeft">
     <div slot="right">
         <component v-for="op in right_top"  :is="op.icon_editor" :ctx="op.icon_ctx"
         @click.native="on_click(op)"></component>
          <van-icon @click.native="actionVisible=true" v-if="rigth_down.length > 0"  name="bars" slot="right" />
    </div>

    </van-nav-bar>
        <van-actionsheet
            v-model="actionVisible"
            :actions="rigth_down"
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
            history.back()
        },
        on_click(op){
            ex.eval(op.action,{ps:this.parStore,head:op})
        },
        //onClickRight(){
        //    if(this.ops.length==1){
        //        let head = this.ops[0]
        //        ex.eval(head.action,{ps:this.parStore,head:head})
        //    }else if(this.ops.length>1){
        //        this.actionVisible = true
        //    }
        //},
        onSelectAction(action){
            ex.eval(action.action,{ps:this.parStore,head:action})
            this.actionVisible =false
        }
    }
})

Vue.component('com-nav-vant-icon',{
    props:['ctx'],
    template:`<div class="com-nav-vant-icon">
      <van-icon  :name="ctx.name" />
    </div>`
})