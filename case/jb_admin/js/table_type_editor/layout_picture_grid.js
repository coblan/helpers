require('./styl/layout_picture_grid.styl')

Vue.component('com-table-layout-picture-grid',{
    template:`<div class="com-table-layout-picture-grid">
    <div class="item" v-for="row in parStore.rows">

        <div class="main-img" >
            <img  :src="row.image_url" alt="">
        </div>

        <input type="checkbox"  :value="row" v-model="parStore.selected">
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
            return  this.parStore.head.title_click
        }
    },
    methods:{
        //is_select(row){
        //    return ex.isin(row,this.parStore.selected)
        //},
        //toggle_row(row){
        //    if(ex.isin(row,this.parStore.selected)){
        //        ex.remove(this.parStore.selected,row)
        //    }else{
        //        this.parStore.selected.push(row)
        //    }
        //},
        on_click(row){
            var ctx = this.parStore.head
            if(ctx.title_click){
                ex.eval(ctx.title_click,{row:row,ctx:ctx,ps:this.parStore})
            }
        }
    }
})