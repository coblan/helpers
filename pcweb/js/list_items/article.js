require('./styl/article.styl')

Vue.component('com-li-article',{
    props:['ctx'],
    template:`<div class="com-li-article">
    <div class="img-ctn" :style="{'background-image':'url('+row.cover+')'}">
    </div>
    <!--<img :src="row.cover" alt="">-->
    <div class="content">
        <span v-if="ctx.click_express" class="title" :class="{clickable:has_action}" v-text="row.title" @click="on_click()"></span>
         <a v-if="ctx.link_express" class="title" :class="{clickable:has_action}" v-text="row.title" :href="get_link()"></a>
        <div class="sub-title" v-text="row.sub_title"></div>
    </div>
    </div>`,
    data(){

        return {
            parStore:ex.vueParStore(this),
            row:this.ctx.row
        }
    },
    computed:{
        has_action(){
            if(this.ctx.click_express){
                return true
            }else{
                return false
            }
        }
    },
    methods:{
        get_link(){
            return ex.eval(this.ctx.link_express,{vc:this})
        },
        on_click(){

            if(this.ctx.click_express){
                ex.eval(this.ctx.click_express,{row:this.row})
            }
        }
    }
})