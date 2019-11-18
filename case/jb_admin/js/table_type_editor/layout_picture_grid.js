require('./styl/layout_picture_grid.styl')

Vue.component('com-table-layout-picture-grid',{
    template:`<div class="com-table-layout-picture-grid">
    <div class="item" v-for="row in parStore.rows">

        <div class="main-img" >
            <img  :src="row.image_url" alt="">
        </div>

        <input type="checkbox">
        <span :class="{clickable:has_action}" v-text="row.image_title" @click="on_click(row)"></span>
    </div>
    </div>`,
    data(){
        return {
            parStore:ex.vueParStore(this)
        }
    },
    mounted(){

    },
    computed:{
        has_action(){
            return  this.parStore.vc.ctx.title_click
        }
    },
    methods:{
        on_click(row){
            if(this.parStore.vc.ctx.title_click){
                ex.eval(this.parStore.vc.ctx.title_click,{row:row})
            }
        }
    }
})