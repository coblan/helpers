require('./styl/table_van_cell.styl')

Vue.component('com-ctn-table-van-cell',{
    props:['heads','rows','option'],
    template:`<div class="com-ctn-table-van-cell">
    <van-cell v-for="row in rows" title="单元格" :is-link="has_nextlevel" clickable>
                <template slot="title">
                    <div class="material-wave content"  @click="on_click(row)">
                        <component :is="head.editor" v-for="head in heads"
                            :class="head.class" :head="head" :row="row"></component>
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
        if(this.option && this.option.style){
            ex.append_css(this.option.style)
        }
    },
    computed:{
        has_nextlevel(){
            if(this.parStore.detail_editor){
                return true
            }else{
                return false
            }
        }
    },
    methods:{
        on_click(row){
            this.$emit('select',row)
        }
    }
})