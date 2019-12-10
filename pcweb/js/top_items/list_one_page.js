require('./styl/list_one_page.styl')

Vue.component('com-ti-list-one-page',{
    props:['ctx'],
    template:`<div class="com-ti-list-one-page">
    <div v-if="ctx.title" class="title" v-text="ctx.title"></div>
    <div >
        <component v-for="row in rows" :is="ctx.item_editor" :ctx="row"></component>
    </div>
    </div>`,
    data(){
        var childStore = new Vue()
        childStore.vc=this
        return {
            childStore:childStore,
            rows:  [],
        }
    },
    mounted(){
        this.search()
    },
    methods:{
        search(){
            return this.get_rows()
        },
        get_rows(){
            return ex.director_call(this.ctx.director_name,{}).then((resp)=>{
                this.rows = resp.rows
            })
        }
    }
})