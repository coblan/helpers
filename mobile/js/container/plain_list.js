require('./styl/plain_list.styl')

Vue.component('com-list-plain',{
    props:['heads','rows'],
    template:`<div class="com-list-plain list-content">
    <van-cell v-for="row in rows" title="单元格" :is-link="parStore.vc.ctx.has_nextlevel" clickable>
                <template slot="title">
                    <div class="material-wave content"  @click="on_click(row)">
                    <span v-for="head in heads" v-text="row[head.name]" class="head.class"></span>
                    </div>
                </template>
     </van-cell>
    </div>`,
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
})